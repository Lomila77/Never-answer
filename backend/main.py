import uvicorn
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.app.weboscket import Model
from backend.app.rag import RAG
from dotenv import load_dotenv
from backend.api.prompt import (
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
rag = RAG("/media/gcolomer/gcolomer/to_load")
model_caller = Model()
logger = logging.getLogger("")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data: str = await websocket.receive_text()
            logger.info(f"Data: {data}")
            user_input: dict = json.loads(data)
            if "audio" in user_input:
                audio_response = await model_caller.groq_voice_chat(
                    user_input["audio"], PROMPT_TEMPLATE)
                await websocket.send_json({"audio": audio_response})
            elif "text" in user_input:
                async for chunk in model_caller.stream_text_response(
                        PROMPT_TEMPLATE, user_input["text"]):
                    logger.info(f"Chunk: {chunk}")
                    await websocket.send_json({"text": chunk})
                # Signale la fin de la génération
                await websocket.send_json({"done": True})
            else:
                raise ValueError("Unproccessable entity")
    except WebSocketDisconnect:
        logger.info("Websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


@app.websocket("/ws/course")
async def websocket_endpoint_course(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data: str = await websocket.receive_text()
            user_query: dict = json.loads(data)
            ressource = rag.similarity_search(user_query["text"])
            logger.info(f"Ressource: {ressource}")
            prompt = PROMPT_TEMPLATE_COURSE.format(rag_document=ressource)
            async for chunk in model_caller.stream_text_response(
                    prompt=prompt, user_query=user_query["text"]):
                await websocket.send_json({"text": chunk})
            await websocket.send_json({"done": True})
    except WebSocketDisconnect:
        logger.info("Websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


@app.websocket("/ws/evaluation")
async def websocket_endpoint_evaluation(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            user_query = await websocket.receive_text()
            # ressource = rag.similarity_search(user_query)
            ressource = ""
            prompt = PROMPT_TEMPLATE_EVALUATION.format(rag_document=ressource)
            async for chunk in model_caller.stream_text_response(
                    prompt=prompt, user_query=user_query):
                response_data = json.loads(chunk)
                await websocket.send_text(response_data["response"])
    except WebSocketDisconnect:
        logger.info("Websocket closed")
    except ValueError as e:
        logger.error(f"{e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
