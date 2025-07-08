from typing import AsyncGenerator
import json
import asyncio
from transformers import AutoTokenizer
import socket
import os
from groq import AsyncGroq, Groq
import numpy as np
from qai_hub_models.models import llama_v3_8b_instruct
from pathlib import Path


# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
# tokenizer.save_pretrained("tokenizer")

class Model:

    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_asyncclient = AsyncGroq(api_key=self.groq_api_key)
        self.groq_client = Groq(api_key=self.groq_api_key)
        self.dlc_model_path = "llama3-8b-4bit.dlc"
        self.output_dir = "output"

    def is_online(self) -> bool:
        """
        Vérifie la connexion à Internet en tentant d'atteindre un DNS public (Cloudflare).
        """
        host: str = "1.1.1.1"
        port: int = 53
        timeout: float = 1.5
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    def groq_speech_to_text(self, audio: bytes) -> str:
        response = self.groq_client.audio.transcriptions.create(
            file=("audio.wav", audio),  # (nom, bytes, type_mime)
            model="whisper-large-v3",
            response_format="json",
            language="en",
            temperature=0.0
        )
        return response.text
            
    def groq_text_to_speech(self, message: str) -> bytes:
        response = self.groq_client.audio.speech.create(
            model="playai-tts",
            voice="Fritz-PlayAI",
            input=message,
            response_format="wav"
        )
        return response.read()

    async def groq_voice_chat(self, audio: bytes, prompt: str) -> bytes:
        if not self.is_online():
            raise ValueError("You need to be online for speech chat")
        voice_to_text: str = self.groq_speech_to_text(audio=audio)
        model_response: str = ""
        async for chunk in self.stream_groq_response(
                prompt=prompt, user_query=voice_to_text):
            model_response += chunk
        audio_response: bytes = self.groq_text_to_speech(
            message=model_response)
        return audio_response

    async def stream_text_response(self, prompt: str, user_query: str, model: str = "llama3-70b-8192") -> AsyncGenerator[str, None]:
        if self.is_online():
            async for chunk in self.stream_groq_response(prompt, user_query, model):
                yield chunk
        else:
            async for chunk in self.stream_local_npu_llama_response(prompt, user_query):
                yield chunk

    async def stream_groq_response(self, prompt: str, user_query: str, model: str = "llama3-70b-8192") -> AsyncGenerator[str, None]:
        prediction_stream = self.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{prompt}"
                },
                {
                    "role": "user",
                    "content": f"{user_query}"
                }
            ],
            model=model,
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=True
        )
        for chunk in prediction_stream:
            await asyncio.sleep(0.03)
            yield chunk.choices[0].delta.content

async def stream_local_npu_llama_response(self, prompt: str, user_query: str) -> AsyncGenerator[str, None]:
    full_prompt = f"{prompt}\n{user_query}"
    model = llama_v3_8b_instruct.model
    response = model(full_prompt)
    # Stream simple char par char (optionnel)
    for word in response.split():
        await asyncio.sleep(0.02)
        yield word + " "