from typing import AsyncGenerator
import json
import httpx
import asyncio
import numpy as np
from transformers import AutoTokenizer
import socket
import os


class Model:

    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Meta-Llama-3-8B-Instruct")

    async def call_model(self, prompt: str = "", audio: str = "") -> AsyncGenerator[str, None]:
        if self.is_online:
            if prompt == "":
                async for chunk in self.stream_groq_speech_chat(audio):
                    yield chunk
            else:
                async for chunk in self.stream_groq_response(prompt):
                    yield chunk
        else:
            async for chunk in self.stream_local_llama_response(prompt):
                yield chunk

    def is_online(self) -> bool:
        """
        Vérifie la connexion à Internet en tentant d'atteindre un DNS public (Cloudflare).
        """
        host: str = "1.1.1.1"
        port: int =53
        timeout: float =1.5
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    async def mock_stream_ollama_response(self) -> AsyncGenerator[str, None]:
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

    async def stream_groq_speech_chat(self, audio_base64: str) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/v1/speech-to-text",
                headers={"Authorization": f"Bearer {self.groq_api_key}"},
                json={"audio": audio_base64, "language": "en"}
            )
            async for chunk in self.stream_groq_response(response.json()["text"]):
                yield chunk

    async def stream_groq_response(self, prompt: str) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                }
            )
            yield json.dumps({"response": response.json()["choices"][0]["message"]["content"]})

    async def stream_local_llama_response(self, prompt: str) -> AsyncGenerator[str, None]:
        command = [
            "./llama.cpp/main",
            "-m", "models/llama3-8b/llama-3-8b-instruct.Q4_K_M.gguf",
            "-p", prompt,
            "-n", "512"
        ]
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )

        output = ""
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            output += line.decode()
            yield json.dumps({"response": output})

    async def stream_local_npu_llama_response(self, prompt: str) -> AsyncGenerator[str, None]:
        tokens = self.tokenizer(
            prompt, return_tensors="np", add_special_tokens=False)["input_ids"]
        input_ids = tokens[0].tolist()
        with open("input.json", "w") as f:
            json.dump({"input_ids": input_ids}, f)
        with open("input_list.txt", "w") as f:
            f.write("input.json\n")

        process = await asyncio.create_subprocess_exec(
            "snpe-net-run",
            "--container", "llama3-8b-instruct.dlc",
            "--input_list", "input_list.txt",
            "--use_dsp",
            "--output_dir", "output",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL
        )
        await process.communicate()

        logits = np.fromfile("output/OUTPUT_0.raw", dtype=np.float32)
        seq_len = len(input_ids)
        vocab_size = logits.size // seq_len
        logits = logits.reshape((1, seq_len, vocab_size))  # [B, T, V]

        preds = np.argmax(logits, axis=-1)[0]
        generated = self.tokenizer.decode(preds)

        yield json.dumps({"response": generated})
