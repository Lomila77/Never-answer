from typing import AsyncGenerator
import json
import asyncio
from transformers import AutoTokenizer
import socket
import os
from groq import AsyncGroq
import random


class Model:

    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_client = AsyncGroq(api_key=self.groq_api_key)
        # self.tokenizer = AutoTokenizer.from_pretrained(
        #     "meta-llama/Meta-Llama-3-8B-Instruct")

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

    async def mock_stream_ollama_response(self) -> AsyncGenerator[str, None]:
        """
        Fonction mock pour simuler des réponses de l'IA.
        """
        fake_responses = [
            json.dumps({"response": "OK."}),
            json.dumps({"response": "Bien sûr !"}),
            json.dumps({"response": "Voici une réponse un peu plus longue pour tester le comportement du chat."}),
            json.dumps({"response": "D'accord, je vais m'en occuper."}),
            json.dumps({"response": "Ceci est un message très court."}),
            json.dumps({"response": "Voici une réponse très détaillée qui explique en plusieurs phrases comment fonctionne le système de mock. Cela permet de vérifier l'affichage des messages longs dans l'interface utilisateur et de s'assurer que tout reste lisible."}),
            json.dumps({"response": "Test."}),
            json.dumps({"response": "Merci pour votre question, je vais y répondre dans un instant."}),
            json.dumps({"response": "Réponse intermédiaire, ni trop longue ni trop courte."}),
            json.dumps({"response": "Ceci est un exemple de message généré aléatoirement pour simuler une interaction avec l'IA dans différents cas d'usage."}),
        ]
        await asyncio.sleep(0.5)  # Simule un délai de streaming
        yield random.choice(fake_responses)

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

    def groq_voice_chat(self, audio: bytes, prompt: str) -> bytes:
        if not self.is_online():
            raise ValueError("You need to be online for speech chat")
        voice_to_text: str = self.groq_speech_to_text(audio=audio)
        model_response: str = self.stream_groq_response(
            prompt=prompt, user_query=voice_to_text)
        audio_response: bytes = self.groq_text_to_speech(
            message=model_response)
        return audio_response

    # TODO: replace the mock by real function
    async def stream_text_response(self, prompt: str, user_query: str, model: str = "llama3-70b-8192") -> AsyncGenerator[str, None]:
        if self.is_online():
            async for chunk in self.stream_groq_response(prompt, user_query, model):
                yield chunk
        else:
            #async for chunk in self.stream_local_npu_llama_response(prompt, user_query):
            async for chunk in self.mock_stream_ollama_response():
                yield chunk

    async def stream_groq_response(self, prompt: str, user_query: str, model: str = "llama3-70b-8192") -> AsyncGenerator[str, None]:
        prediction_stream = await self.groq_client.chat.completions.create(
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
        async for chunk in prediction_stream:
            await asyncio.sleep(0.03)
            yield chunk.choices[0].delta.content

    # TODO: On attends la machine pour tester
    # async def stream_local_npu_llama_response(self, prompt: str, user_query: str) -> AsyncGenerator[str, None]:
    #     tokens = self.tokenizer(
    #         prompt + user_query, return_tensors="np", add_special_tokens=False)["input_ids"]
    #     input_ids = tokens[0].tolist()
    #     with open("input.json", "w") as f:
    #         json.dump({"input_ids": input_ids}, f)
    #     with open("input_list.txt", "w") as f:
    #         f.write("input.json\n")

    #     process = await asyncio.create_subprocess_exec(
    #         "snpe-net-run",
    #         "--container", "llama3-8b-instruct.dlc",
    #         "--input_list", "input_list.txt",
    #         "--use_dsp",
    #         "--output_dir", "output",
    #         stdout=asyncio.subprocess.PIPE,
    #         stderr=asyncio.subprocess.DEVNULL
    #     )
    #     await process.communicate()

    #     logits = np.fromfile("output/OUTPUT_0.raw", dtype=np.float32)
    #     seq_len = len(input_ids)
    #     vocab_size = logits.size // seq_len
    #     logits = logits.reshape((1, seq_len, vocab_size))  # [B, T, V]

    #     preds = np.argmax(logits, axis=-1)[0]
    #     generated = self.tokenizer.decode(preds)

    #     yield json.dumps({"response": generated})
