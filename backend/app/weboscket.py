from typing import AsyncGenerator, Optional
import json
import asyncio
from transformers import AutoTokenizer
import socket
import os
from groq import AsyncGroq, Groq
import numpy as np
from pathlib import Path
import logging
from app.memory import MemoryManager



# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
# tokenizer.save_pretrained("tokenizer")from app.memory import MemoryManager


class Model:

    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_async_client = AsyncGroq(api_key=self.groq_api_key)
        self.groq_client = Groq(api_key=self.groq_api_key)
        self.dlc_model_path = "llama3-8b-4bit.dlc"
        self.output_dir = "output"
        self.memory_manager = MemoryManager()

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

    async def groq_voice_chat(self, audio: bytes, prompt: str, session_id: str) -> bytes:
        if not self.is_online():
            raise ValueError("You need to be online for speech chat")
        voice_to_text: str = self.groq_speech_to_text(audio=audio)
        
        # Add user message to memory
        self.memory_manager.add_user_message(session_id, voice_to_text)
        chat_response = ""
        async for chunk in self.stream_groq_response_with_memory(
            prompt=prompt, user_query=voice_to_text, session_id=session_id):
            chat_response += chunk
        
        audio_response: bytes = self.groq_text_to_speech(
            message=chat_response)

        return audio_response

    # TODO: replace the mock by real function
    async def stream_text_response(self, prompt: str, user_query: str, model: str = "llama3-70b-8192", session_id: Optional[str] = None) -> AsyncGenerator[str, None]:
        if session_id:
            self.memory_manager.add_user_message(session_id, user_query)
            
            # Get chat history and add to prompt if session_id is provided
            chat_history = ""
            if session_id in self.memory_manager.memories:
                chat_history = self.memory_manager.get_chat_history(session_id)
                
            # Format the prompt with chat history if it has the {chat_history} placeholder
            if "{chat_history}" in prompt:
                prompt = prompt.format(chat_history=f"Historique de la conversation :\n{chat_history}" if chat_history else "", rag_document="")
            
        if self.is_online():
            collected_chunks = []
            async for chunk in self.stream_groq_response_with_memory(prompt, user_query, model, session_id):
                collected_chunks.append(chunk)
                yield chunk
                
            if session_id:
                # Join all chunks to form the complete AI response
                complete_response = "".join([chunk for chunk in collected_chunks if chunk])
                if complete_response:
                    self.memory_manager.add_ai_message(session_id, complete_response)
        else:
            async for chunk in self.stream_local_npu_llama_response(prompt, user_query):
                yield chunk

    async def stream_groq_response_with_memory(self, prompt: str, user_query: str, model: str = "llama3-70b-8192", session_id: Optional[str] = None) -> AsyncGenerator[str, None]:
        # Prepare messages with memory if session_id is provided
        messages = [
            {
                "role": "system",
                "content": f"{prompt}"
            }
        ]
        # Add conversation history if session_id is provided
        if session_id:
            chat_history = self.memory_manager.get_chat_history(session_id)
            # Include chat history in the system prompt
            messages[0]["content"] += f"\n\nConversation history:\n{chat_history}"

        # Add current user query
        messages.append({
            "role": "user",
            "content": f"{user_query}"
        })

        prediction_stream = await self.groq_async_client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=True
        )
        
        async for chunk in prediction_stream:
            await asyncio.sleep(0.03)
            content = chunk.choices[0].delta.content
            if content:
                yield content

    # async def stream_local_npu_llama_response(self, prompt: str, user_query: str) -> AsyncGenerator[str, None]:
    #     text_input = prompt + user_query
    #     tokens = self.tokenizer(text_input, return_tensors="np", add_special_tokens=False)["input_ids"]
    #     input_ids = tokens[0].tolist()

    #     # Préparation fichiers
    #     Path("input").mkdir(exist_ok=True)
    #     with open("input/input.json", "w") as f:
    #         json.dump({"input_ids": input_ids}, f)
    #     with open("input/input_list.txt", "w") as f:
    #         f.write("input/input.json\n")

    #     # Lancement SNPE
    #     process = await asyncio.create_subprocess_exec(
    #         "snpe-net-run",
    #         "--container", self.dlc_model_path,
    #         "--input_list", "input/input_list.txt",
    #         "--use_dsp",
    #         "--output_dir", self.output_dir,
    #         stdout=asyncio.subprocess.PIPE,
    #         stderr=asyncio.subprocess.DEVNULL
    #     )
    #     await process.communicate()

    #     # Lecture sortie
    #     output_path = os.path.join(self.output_dir, "OUTPUT_0.raw")
    #     logits = np.fromfile(output_path, dtype=np.float32)
    #     vocab_size = self.tokenizer.vocab_size
    #     seq_len = len(input_ids)
    #     logits = logits.reshape((1, seq_len, vocab_size))  # [1, T, V]

    #     preds = np.argmax(logits, axis=-1)[0]
    #     decoded = self.tokenizer.decode(preds)

    #     yield json.dumps({"response": decoded})