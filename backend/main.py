import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data: str = await websocket.receive_text()
            user_input: dict = json.load(data)
            if "audio" in user_input:
                audio_response = model_caller.groq_voice_chat(
                    user_input["audio"], PROMPT_TEMPLATE)
                await websocket.send_json({"audio": audio_response})
            elif "text" in user_input:
                async for chunk in model_caller.stream_text_response(
                        PROMPT_TEMPLATE, user_input["text"]):
                    text_response = json.loads(chunk)
                    await websocket.send_json({"text": text_response})
            else:
                raise ValueError("Unproccessable entity")
    except WebSocketDisconnect:
        print("Websocket disconnected")
        return {"success": "Webscocket closed"}
    except ValueError as e:
        print(e)
        return {"error": e}
    finally:
        await websocket.close()


@app.websocket("/ws/course")
async def websocket_endpoint_course(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            user_query = await websocket.receive_text()
            ressource = rag.similarity_search(user_query)
            prompt = PROMPT_TEMPLATE_COURSE.format(rag_document=ressource)
            async for chunk in model_caller.stream_text_response(
                    prompt=prompt, user_query=user_query):
                response_data = json.loads(chunk)
                await websocket.send_text(response_data["response"])
    except WebSocketDisconnect:
        print("Websocket disconnected")
        return {"success": "Webscocket closed"}
    except ValueError as e:
        print(e)
        return {"error": e}
    finally:
        await websocket.close()


@app.websocket("/ws/evaluation")
async def websocket_endpoint_evaluation(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            user_query = await websocket.receive_text()
            ressource = rag.similarity_search(user_query)
            prompt = PROMPT_TEMPLATE_EVALUATION.format(rag_document=ressource)
            async for chunk in model_caller.stream_text_response(
                    prompt=prompt, user_query=user_query):
                response_data = json.loads(chunk)
                await websocket.send_text(response_data["response"])
    except WebSocketDisconnect:
        print("Websocket disconnected")
        return {"success": "Webscocket closed"}
    except ValueError as e:
        print(e)
        return {"error": e}
    finally:
        await websocket.close()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
