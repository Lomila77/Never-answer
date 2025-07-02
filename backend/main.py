import logging
from fastapi import FastAPI, WebSocket
import uvicorn
from backend.app.weboscket import stream_ollama_response

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
        async for chunk in stream_ollama_response(data):
            await websocket.send_text(chunk["response"])
            if chunk["done"]:
                break


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
