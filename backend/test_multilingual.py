import asyncio
import json
import websockets
import logging
from dotenv import load_dotenv

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 加載環境變數
load_dotenv()

async def test_multilingual_responses():
    """測試AI對不同語言的回應能力"""
    uri = "ws://localhost:8000/ws"
    logger.info("開始測試多語言功能")
    
    try:
        # 連接WebSocket
        async with websockets.connect(uri) as websocket:
            # 測試中文
            await test_language(websocket, "zh", "你好，我想學習數學。")
            
            # 測試英文
            await test_language(websocket, "en", "Hello, I want to learn mathematics.")
            
            # 測試法文
            await test_language(websocket, "fr", "Bonjour, je veux apprendre les mathématiques.")
            
    except Exception as e:
        logger.error(f"測試過程中發生錯誤: {str(e)}")
    
    logger.info("多語言測試完成")

async def test_language(websocket, language_code, message):
    """測試特定語言的回應"""
    logger.info(f"測試 {language_code} 語言: '{message}'")
    
    # 發送消息
    await websocket.send(json.dumps({"text": message}))
    
    # 接收回應
    full_response = ""
    while True:
        response = await websocket.recv()
        data = json.loads(response)
        
        if "done" in data and data["done"]:
            break
            
        if "text" in data:
            full_response += data["text"]
            
        if "error" in data:
            logger.error(f"接收到錯誤: {data['error']}")
            break
    
    logger.info(f"{language_code} 回應: {full_response[:100]}...")
    
    # 清除記憶，為下一個測試準備
    await websocket.send(json.dumps({"clear_memory": True}))
    clear_response = await websocket.recv()
    logger.info(f"清除記憶回應: {clear_response}")
    
    return full_response

if __name__ == "__main__":
    asyncio.run(test_multilingual_responses()) 