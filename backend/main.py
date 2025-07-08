import uvicorn
import json
import logging
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.weboscket import Model
from app.rag import RAG
from dotenv import load_dotenv
from api.prompt import (
    PROMPT_TEMPLATE,
    PROMPT_TEMPLATE_COURSE,
    PROMPT_TEMPLATE_EVALUATION
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
load_dotenv()

app = FastAPI()
rag = RAG("./db")  # Change to a relative path pointing to the existing db directory
model_caller = Model()
logger = logging.getLogger("")

# Dictionary to store websocket session IDs
session_store = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        # Create a unique session ID for this websocket connection
        session_id = str(uuid.uuid4())
        session_store[id(websocket)] = session_id
        logger.info(f"New websocket connection established with session ID: {session_id}")
        
        while True:
            data: str = await websocket.receive_text()
            logger.info(f"Data: {data}")
            user_input: dict = json.loads(data)
            if "audio" in user_input:
                audio_response = await model_caller.groq_voice_chat(
                    user_input["audio"], PROMPT_TEMPLATE.format(chat_history="{chat_history}"), session_id)
                await websocket.send_json({"audio": audio_response})
            elif "text" in user_input:
                # Format prompt with placeholder for chat history
                prompt_with_history = PROMPT_TEMPLATE.format(chat_history="{chat_history}")
                
                async for chunk in model_caller.stream_text_response(
                        prompt_with_history, user_input["text"], session_id=session_id):
                    logger.info(f"Chunk: {chunk}")
                    await websocket.send_json({"text": chunk})
                # Signale la fin de la génération
                await websocket.send_json({"done": True})
            else:
                raise ValueError("Unproccessable entity")
    except WebSocketDisconnect:
        # Clean up the session when the websocket disconnects
        if id(websocket) in session_store:
            del session_store[id(websocket)]
        logger.info("Websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


@app.websocket("/ws/course")
async def websocket_endpoint_course(websocket: WebSocket):
    try:
        await websocket.accept()
        # Create a unique session ID for this websocket connection
        session_id = str(uuid.uuid4())
        session_store[id(websocket)] = session_id
        logger.info(f"New course websocket connection established with session ID: {session_id}")
        
        while True:
            data: str = await websocket.receive_text()
            user_query: dict = json.loads(data)
            ressource = rag.similarity_search(user_query["text"])
            logger.info(f"Ressource: {ressource}")
            
            # The prompt will be formatted with chat_history in the stream_text_response method
            # Just need to pass the RAG document content here
            prompt = PROMPT_TEMPLATE_COURSE.format(rag_document=ressource, chat_history="{chat_history}")
            
            async for chunk in model_caller.stream_text_response(
                    prompt=prompt, user_query=user_query["text"], session_id=session_id):
                await websocket.send_json({"text": chunk})
            await websocket.send_json({"done": True})
    except WebSocketDisconnect:
        # Clean up the session when the websocket disconnects
        if id(websocket) in session_store:
            del session_store[id(websocket)]
        logger.info("Websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


@app.websocket("/ws/evaluation")
async def websocket_endpoint_evaluation(websocket: WebSocket):
    try:
        await websocket.accept()
        # Create a unique session ID for this websocket connection
        session_id = str(uuid.uuid4())
        session_store[id(websocket)] = session_id
        logger.info(f"New evaluation websocket connection established with session ID: {session_id}")
        
        while True:
            user_query = await websocket.receive_text()
            # ressource = rag.similarity_search(user_query)
            ressource = ""
            
            # Format with placeholder for chat history
            prompt = PROMPT_TEMPLATE_EVALUATION.format(rag_document=ressource, chat_history="{chat_history}")
            
            async for chunk in model_caller.stream_text_response(
                    prompt=prompt, user_query=user_query, session_id=session_id):
                response_data = json.loads(chunk)
                await websocket.send_text(response_data["response"])
    except WebSocketDisconnect:
        # Clean up the session when the websocket disconnects
        if id(websocket) in session_store:
            del session_store[id(websocket)]
        logger.info("Websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


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