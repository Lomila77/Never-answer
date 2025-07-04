from typing import AsyncGenerator
import json
from backend.api.prompt import PROMPT_TEMPLATE
import httpx


# TODO: Changer le model ? Refaire un prompt ?
async def stream_ollama_response(message: str) -> AsyncGenerator[str, None]:
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": PROMPT_TEMPLATE + message,
                "stream": True,
            },
        ) as response:
            async for chunk in response.aiter_lines():
                yield json.loads(chunk)


async def mock_stream_ollama_response(message: str) -> AsyncGenerator[str, None]:
    """
    Fonction mock pour simuler des réponses de l'IA.
    """
    import asyncio
    fake_responses = [
        json.dumps({"response": "Ceci est une réponse simulée 1."}),
        json.dumps({"response": "Ceci est une réponse simulée 2."}),
        json.dumps({"response": "Ceci est une réponse simulée 3."}),
    ]
    for fake in fake_responses:
        await asyncio.sleep(0.5)  # Simule un délai de streaming
        yield fake
