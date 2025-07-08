import uvicorn
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from app.weboscket import Model
from app.rag import RAG
from app.memory import MemoryManager
from dotenv import load_dotenv
from api.prompt import (
    PROMPT_TEMPLATE,
    PROMPT_TEMPLATE_COURSE,
    PROMPT_TEMPLATE_EVALUATION
)
from app.utils import is_wav_bytes
import base64
import os
import uuid
from typing import Dict, Optional


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
load_dotenv()

app = FastAPI()
# 修正Windows路徑
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "db")
if not os.path.exists(db_path):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "db1")

rag = RAG(db_path)
model_caller = Model()
memory_manager = MemoryManager()
logger = logging.getLogger(__name__)

# 追蹤活躍的WebSocket連接
active_connections: Dict[str, WebSocket] = {}


def preprocess_audio_data(audio_b64: str) -> bytes:
    """
    預處理Base64編碼的音頻數據
    
    Args:
        audio_b64: Base64編碼的音頻數據
        
    Returns:
        解碼後的音頻字節數據
    """
    logger.info(f"處理音頻數據，長度: {len(audio_b64)}")
    
    # 檢查並處理可能的data URL格式
    if ',' in audio_b64:
        logger.info("檢測到data URL格式，提取Base64部分")
        # 如果是data URL格式 (例如 "data:audio/wav;base64,...")
        audio_b64 = audio_b64.split(',', 1)[1]
    
    # 確保Base64字符串長度是4的倍數
    padding_needed = len(audio_b64) % 4
    if padding_needed:
        logger.info(f"添加 {4 - padding_needed} 個padding字符")
        audio_b64 += '=' * (4 - padding_needed)
    
    # 解碼Base64數據
    try:
        audio_bytes = base64.b64decode(audio_b64)
        logger.info(f"成功解碼Base64數據，得到 {len(audio_bytes)} 字節")
        return audio_bytes
    except Exception as e:
        logger.error(f"Base64解碼失敗: {str(e)}")
        # 嘗試移除可能的非法字符
        logger.info("嘗試清理Base64字符串")
        # 只保留有效的Base64字符
        valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        audio_b64 = ''.join(c for c in audio_b64 if c in valid_chars)
        
        # 再次確保長度是4的倍數
        padding_needed = len(audio_b64) % 4
        if padding_needed:
            audio_b64 += '=' * (4 - padding_needed)
        
        # 再次嘗試解碼
        audio_bytes = base64.b64decode(audio_b64)
        logger.info(f"清理後成功解碼Base64數據，得到 {len(audio_bytes)} 字節")
        return audio_bytes


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 為每個WebSocket連接生成一個唯一的會話ID
    session_id = str(uuid.uuid4())
    try:
        await websocket.accept()
        active_connections[session_id] = websocket
        logger.info(f"新的WebSocket連接已建立，會話ID: {session_id}")
        
        while True:
            data: str = await websocket.receive_text()
            user_input: dict = json.loads(data)
            
            if "audio" in user_input:
                # 音頻處理
                try:
                    audio_b64 = user_input["audio"]
                    
                    # 預處理音頻數據
                    try:
                        audio_bytes = preprocess_audio_data(audio_b64)
                    except Exception as e:
                        logger.error(f"音頻預處理失敗: {str(e)}")
                        await websocket.send_json({"error": f"音頻數據格式錯誤: {str(e)}"})
                        continue
                    
                    # 檢查是否為WAV格式
                    if not is_wav_bytes(audio_bytes):
                        logger.warning(f"收到的不是WAV格式，頭部: {audio_bytes[:16]}")
                        # 即使不是WAV格式，也嘗試處理
                        logger.info("嘗試處理非WAV格式音頻")
                    
                    # 處理音頻請求並加入記憶
                    chat_history = memory_manager.get_chat_history(session_id)
                    full_prompt = PROMPT_TEMPLATE.format(chat_history=chat_history)
                    
                    logger.info("開始處理語音對話")
                    audio_response = await model_caller.groq_voice_chat(
                        audio_bytes, full_prompt, session_id)
                    
                    # 將音頻轉換為base64並發送
                    response_b64 = base64.b64encode(audio_response).decode("utf-8")
                    logger.info(f"生成的音頻回應大小: {len(response_b64)}")
                    await websocket.send_json({"audio": response_b64})
                    logger.info("音頻回應已發送")
                    await websocket.send_json({"done": True})
                except Exception as e:
                    logger.error(f"處理音頻時發生錯誤: {str(e)}")
                    await websocket.send_json({"error": str(e)})
                    
            elif "text" in user_input:
                # 文本處理
                try:
                    # 將用戶消息添加到記憶
                    user_message = user_input["text"]
                    memory_manager.add_user_message(session_id, user_message)
                    
                    # 獲取聊天歷史
                    chat_history = memory_manager.get_chat_history(session_id)
                    full_prompt = PROMPT_TEMPLATE.format(chat_history=chat_history)
                    
                    # 流式響應
                    ai_response = ""
                    async for chunk in model_caller.stream_text_response(
                            full_prompt, user_message, "llama3-70b-8192", session_id):
                        logger.info(f"Chunk: {chunk}")
                        ai_response += chunk
                        await websocket.send_json({"text": chunk})
                    
                    # 將AI響應添加到記憶
                    memory_manager.add_ai_message(session_id, ai_response)
                    
                    # 告知客戶端生成完成
                    await websocket.send_json({"done": True})
                except Exception as e:
                    logger.error(f"處理文本時發生錯誤: {str(e)}")
                    await websocket.send_json({"error": str(e)})
            
            elif "clear_memory" in user_input and user_input["clear_memory"]:
                # 清除記憶
                try:
                    memory_manager.clear_memory(session_id)
                    await websocket.send_json({"result": "記憶已清除", "success": True})
                except Exception as e:
                    logger.error(f"清除記憶時發生錯誤: {str(e)}")
                    await websocket.send_json({"error": str(e)})
            
            else:
                raise ValueError("Unproccessable entity")
    except WebSocketDisconnect:
        logger.info(f"WebSocket已關閉，會話ID: {session_id}")
        if session_id in active_connections:
            del active_connections[session_id]
    except ValueError as e:
        logger.error(f"{e}")
        if session_id in active_connections:
            del active_connections[session_id]


@app.websocket("/ws/course")
async def websocket_endpoint_course(websocket: WebSocket):
    session_id = str(uuid.uuid4())
    try:
        await websocket.accept()
        active_connections[session_id] = websocket
        
        while True:
            data: str = await websocket.receive_text()
            user_query: dict = json.loads(data)
            
            # 獲取RAG結果和用戶消息
            ressource = rag.similarity_search(user_query["text"])
            logger.info(f"Ressource: {ressource}")
            
            # 將用戶消息添加到記憶
            memory_manager.add_user_message(session_id, user_query["text"])
            chat_history = memory_manager.get_chat_history(session_id)
            
            # 完整提示詞
            prompt = PROMPT_TEMPLATE_COURSE.format(
                chat_history=chat_history,
                rag_document=ressource
            )
            
            # 生成回復
            ai_response = ""
            async for chunk in model_caller.stream_text_response(
                    prompt=prompt, user_query=user_query["text"], model="llama3-70b-8192", session_id=session_id):
                ai_response += chunk
                await websocket.send_json({"text": chunk})
            
            # 添加AI回應到記憶
            memory_manager.add_ai_message(session_id, ai_response)
            await websocket.send_json({"done": True})
    except WebSocketDisconnect:
        logger.info(f"WebSocket已關閉，會話ID: {session_id}")
        if session_id in active_connections:
            del active_connections[session_id]
    except ValueError as e:
        logger.error(f"{e}")
        if session_id in active_connections:
            del active_connections[session_id]


@app.websocket("/ws/evaluation")
async def websocket_endpoint_evaluation(websocket: WebSocket):
    session_id = str(uuid.uuid4())
    try:
        await websocket.accept()
        active_connections[session_id] = websocket
        
        while True:
            data: str = await websocket.receive_text()
            user_query: dict = json.loads(data)
            
            # 獲取RAG資源和用戶消息
            ressource = rag.similarity_search(user_query["text"])
            logger.info(f"Ressource: {ressource}")
            
            # 將用戶消息添加到記憶
            memory_manager.add_user_message(session_id, user_query["text"])
            chat_history = memory_manager.get_chat_history(session_id)
            
            # 完整提示詞
            prompt = PROMPT_TEMPLATE_EVALUATION.format(
                chat_history=chat_history, 
                rag_document=ressource
            )
            
            # 生成回復
            ai_response = ""
            async for chunk in model_caller.stream_text_response(
                    prompt=prompt, user_query=user_query["text"], model="llama3-70b-8192", session_id=session_id):
                ai_response += chunk
                await websocket.send_json({"text": chunk})
            
            # 添加AI回應到記憶
            memory_manager.add_ai_message(session_id, ai_response)
            await websocket.send_json({"done": True})
    except WebSocketDisconnect:
        logger.info(f"WebSocket已關閉，會話ID: {session_id}")
        if session_id in active_connections:
            del active_connections[session_id]
    except ValueError as e:
        logger.error(f"{e}")
        if session_id in active_connections:
            del active_connections[session_id]


@app.get("/api/clear_memory")
async def clear_memory_endpoint(session_id: Optional[str] = None):
    """清除指定會話或所有會話的記憶"""
    try:
        if session_id:
            memory_manager.clear_memory(session_id)
            return {"result": f"已清除會話 {session_id} 的記憶", "success": True}
        else:
            # 清除所有活躍會話的記憶
            for sid in active_connections.keys():
                memory_manager.clear_memory(sid)
            return {"result": "已清除所有會話的記憶", "success": True}
    except Exception as e:
        logger.error(f"清除記憶時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)