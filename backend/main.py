import uvicorn
import json
import logging
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.weboscket import Model
from app.rag import RAG
from dotenv import load_dotenv
from backend.app.prompt import (
    PROMPT_TEMPLATE,
    PROMPT_TEMPLATE_COURSE,
    PROMPT_TEMPLATE_EVALUATION
)
from backend.app.utils import is_wav_bytes
import base64


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
load_dotenv()

app = FastAPI()
rag = RAG("./db")  # Change to a relative path pointing to the existing db directory
model_caller = Model()
logger = logging.getLogger("")

session_store = {}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        session_id = str(uuid.uuid4())
        session_store[id(websocket)] = session_id
        logger.info(f"New websocket connection established with session ID: {session_id}")

        while True:
            data: str = await websocket.receive_text()
            user_input: dict = json.loads(data)
            chat_history = model_caller.memory_manager.get_chat_history(session_id)
            logger.info(f"Chat history récupéré: {chat_history}")
            
            if "audio" in user_input:
                audio_b64 = user_input["audio"]
                audio_bytes = base64.b64decode(audio_b64)
                if not is_wav_bytes(audio_bytes):
                    logger.error(f"Header reçu : {audio_bytes[:16]}")
                    raise ValueError("Le fichier audio reçu n'est pas au format WAV.")
                audio_response = await model_caller.groq_voice_chat(
                    audio_bytes, 
                    PROMPT_TEMPLATE.format(chat_history=chat_history), 
                    session_id
                )
                audio_b64 = base64.b64encode(audio_response).decode("utf-8")
                await websocket.send_json({"audio": audio_b64})
                logger.info("Audio send")
                await websocket.send_json({"done": True})
            elif "text" in user_input:
                prompt_with_history = PROMPT_TEMPLATE.format(
                    chat_history=chat_history
                )
                
                async for chunk in model_caller.stream_text_response(
                        prompt_with_history, user_input["text"], session_id=session_id):
                    await websocket.send_json({"text": chunk})
                await websocket.send_json({"done": True})
            else:
                raise ValueError("Unproccessable entity")
    except WebSocketDisconnect:
        if id(websocket) in session_store:
            del session_store[id(websocket)]
        logger.info("Websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


@app.websocket("/ws/course")
async def websocket_endpoint_course(websocket: WebSocket):
    try:
        await websocket.accept()
        session_id = str(uuid.uuid4())
        session_store[id(websocket)] = session_id
        logger.info(f"New course websocket connection established with session ID: {session_id}")
        
        while True:
            data: str = await websocket.receive_text()
            user_input: dict = json.loads(data)
            chat_history = model_caller.memory_manager.get_chat_history(session_id)
            logger.info(f"Chat history récupéré: {chat_history}")
            if "audio" in user_input:
                audio_b64 = user_input["audio"]
                audio_bytes = base64.b64decode(audio_b64)
                if not is_wav_bytes(audio_bytes):
                    logger.error(f"Header reçu : {audio_bytes[:16]}")
                    raise ValueError("Le fichier audio reçu n'est pas au format WAV.")
                audio_response = await model_caller.groq_voice_chat(
                    audio_bytes, 
                    PROMPT_TEMPLATE.format(chat_history=chat_history), 
                    session_id
                )
                audio_b64 = base64.b64encode(audio_response).decode("utf-8")
                await websocket.send_json({"audio": audio_b64})
                logger.info("Audio send")
                await websocket.send_json({"done": True})
            elif "text" in user_input:
                logger.info(f"Course - Chat history: {chat_history}")
                
                ressource = rag.similarity_search(user_input["text"])
                logger.info(f"Ressource RAG: {ressource[:200]}...")
                
                prompt = PROMPT_TEMPLATE_COURSE.format(
                    rag_document=ressource, 
                    chat_history=chat_history
                )
                
                async for chunk in model_caller.stream_text_response(
                        prompt=prompt, user_query=user_input["text"], session_id=session_id):
                    await websocket.send_json({"text": chunk})
                await websocket.send_json({"done": True})
    except WebSocketDisconnect:
        if id(websocket) in session_store:
            del session_store[id(websocket)]
        logger.info("Websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


@app.websocket("/ws/evaluation")
async def websocket_endpoint_evaluation(websocket: WebSocket):
    try:
        await websocket.accept()
        session_id = str(uuid.uuid4())
        session_store[id(websocket)] = session_id
        logger.info(f"New evaluation websocket connection established with session ID: {session_id}")
        
        while True:
            data: str = await websocket.receive_text()
            user_input: dict = json.loads(data)
            chat_history = model_caller.memory_manager.get_chat_history(session_id)
            logger.info(f"Chat history récupéré: {chat_history}")
            if "audio" in user_input:
                audio_b64 = user_input["audio"]
                audio_bytes = base64.b64decode(audio_b64)
                if not is_wav_bytes(audio_bytes):
                    logger.error(f"Header reçu : {audio_bytes[:16]}")
                    raise ValueError("Le fichier audio reçu n'est pas au format WAV.")
                audio_response = await model_caller.groq_voice_chat(
                    audio_bytes, 
                    PROMPT_TEMPLATE.format(chat_history=chat_history), 
                    session_id
                )
                audio_b64 = base64.b64encode(audio_response).decode("utf-8")
                await websocket.send_json({"audio": audio_b64})
                logger.info("Audio send")
                await websocket.send_json({"done": True})
            elif "text" in user_input:
                chat_history = model_caller.memory_manager.get_chat_history(session_id)
                logger.info(f"Evaluation - Chat history: {chat_history}")
                
                ressource = rag.similarity_search(user_input["text"])
                logger.info(f"Evaluation - Ressource RAG: {ressource[:200]}...")
                
                prompt = PROMPT_TEMPLATE_EVALUATION.format(
                    rag_document=ressource, 
                    chat_history=chat_history
                )
                
                async for chunk in model_caller.stream_text_response(
                        prompt=prompt, user_query=user_input["text"], session_id=session_id):
                    await websocket.send_json({"text": chunk})
                await websocket.send_json({"done": True})
            
    except WebSocketDisconnect:
        if id(websocket) in session_store:
            del session_store[id(websocket)]
        logger.info("Evaluation websocket closed")
    except json.JSONDecodeError as e:
        logger.error(f"Erreur JSON dans evaluation: {e}")
        await websocket.send_json({"error": "Erreur de format JSON"})
    except Exception as e:
        logger.error(f"Erreur dans evaluation websocket: {e}")
        await websocket.send_json({"error": str(e)})


@app.websocket("/ws/clear-memory")
async def websocket_clear_memory(websocket: WebSocket):
    """Endpoint to clear the conversation memory for a specific session."""
    try:
        await websocket.accept()
        while True:
            # Get the session ID from the request
            data: str = await websocket.receive_text()
            session_data: dict = json.loads(data)
            
            if "session_id" in session_data:
                session_id = session_data["session_id"]
                # Clear memory for the specified session
                model_caller.memory_manager.clear_memory(session_id)
                await websocket.send_json({"status": "success", "message": f"Memory cleared for session {session_id}"})
            else:
                await websocket.send_json({"status": "error", "message": "No session_id provided"})
                
    except WebSocketDisconnect:
        logger.info("Memory clear websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)