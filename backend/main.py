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
rag = RAG("/media/gcolomer/gcolomer/archive/enwiki20201020/")
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
        data = await websocket.receive_text()
        prompt = PROMPT_TEMPLATE.format(user_query=data)
        async for chunk in model_caller.call_model(prompt=prompt):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


@app.websocket("/ws/course")
async def websocket_endpoint_course(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        ressource = rag.similarity_search(data)
        prompt = PROMPT_TEMPLATE_COURSE.format(rag_document=ressource, user_query=data)
        async for chunk in model_caller.call_model(prompt=prompt):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


@app.websocket("/ws/evaluation")
async def websocket_endpoint_evaluation(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        ressource = rag.similarity_search(data)
        prompt = PROMPT_TEMPLATE_EVALUATION.format(rag_document=ressource, user_query=data)
        async for chunk in model_caller.call_model(prompt=prompt):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


@app.websocket("/ws/voice-chat-groq")
async def websocket_voice_chat_groq(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_audio = await websocket.receive_text()
        async for chunk in model_caller.call_model(audio=user_audio):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
