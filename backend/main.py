import logging
from fastapi import FastAPI, WebSocket
import uvicorn
from backend.app.weboscket import Model
import json
from backend.api.prompt import PROMPT_TEMPLATE, PROMPT_TEMPLATE_COURSE, PROMPT_TEMPLATE_EVALUATION
from backend.app.rag import RAG
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
#rag = RAG("/media/gcolomer/gcolomer/archive/enwiki20201020/")
model_caller = Model()


@app.post("/")
def main() -> dict[str, str]:
    try:
        pass
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": str(e)}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_query = await websocket.receive_text()
        async for chunk in model_caller.stream_text_response(
                prompt=PROMPT_TEMPLATE, user_query=user_query):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


@app.websocket("/ws/course")
async def websocket_endpoint_course(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_query = await websocket.receive_text()
        # ressource = rag.similarity_search(user_query)
        ressource = ""
        prompt = PROMPT_TEMPLATE_COURSE.format(rag_document=ressource)
        async for chunk in model_caller.stream_text_response(
                prompt=prompt, user_query=user_query):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


@app.websocket("/ws/evaluation")
async def websocket_endpoint_evaluation(websocket: WebSocket):
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


@app.post("/speech")
def voice_chat(audio: bytes):
    return model_caller.groq_voice_chat(audio=audio, prompt=PROMPT_TEMPLATE)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
