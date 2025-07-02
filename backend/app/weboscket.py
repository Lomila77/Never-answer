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
            json={"model": "llama3", "prompt": PROMPT_TEMPLATE + message},
        ) as response:
            async for chunk in response.aiter_lines():
                yield json.loads(chunk)
