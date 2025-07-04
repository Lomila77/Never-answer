import logging
from fastapi import FastAPI, WebSocket
import uvicorn
from backend.app.weboscket import stream_ollama_response, mock_stream_ollama_response
import json
from backend.api.prompt import PROMPT_TEMPLATE, PROMPT_TEMPLATE_COURSE, PROMPT_TEMPLATE_EVALUATION
app = FastAPI()


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
        prompt = PROMPT_TEMPLATE + data
        async for chunk in mock_stream_ollama_response(prompt):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


@app.websocket("/ws/course")
async def websocket_endpoint_course(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        prompt = PROMPT_TEMPLATE_COURSE + data
        async for chunk in mock_stream_ollama_response(prompt):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


@app.websocket("/ws/evaluation")
async def websocket_endpoint_evaluation(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        prompt = PROMPT_TEMPLATE_EVALUATION + data
        async for chunk in mock_stream_ollama_response(prompt):
            response_data = json.loads(chunk)
            await websocket.send_text(response_data["response"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
