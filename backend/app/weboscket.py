from typing import AsyncGenerator, Optional
import json
import asyncio
from transformers import AutoTokenizer
import socket
import os
from groq import AsyncGroq
import random
from app.memory import MemoryManager
import tempfile
import logging
import io

logger = logging.getLogger(__name__)

class Model:

    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_client = AsyncGroq(api_key=self.groq_api_key)
        # self.tokenizer = AutoTokenizer.from_pretrained(
        #     "meta-llama/Meta-Llama-3-8B-Instruct")
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

    async def groq_speech_to_text(self, audio: bytes) -> str:
        """
        將音頻轉換為文本，使用臨時文件處理音頻數據
        """
        try:
            # 檢查音頻數據
            logger.info(f"收到音頻數據，大小: {len(audio)} 字節")
            if len(audio) < 100:
                logger.error(f"音頻數據太小: {audio}")
                raise ValueError("音頻數據太小，無法處理")
            
            # 創建臨時文件來存儲音頻數據
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio)
                temp_file_path = temp_file.name
            
            logger.info(f"臨時音頻文件已創建: {temp_file_path}")
            
            # 嘗試使用文件對象
            try:
                with open(temp_file_path, "rb") as audio_file:
                    response = await self.groq_client.audio.transcriptions.create(
                        file=audio_file,
                        model="whisper-large-v3",
                        response_format="json",
                        language="en",
                        temperature=0.0
                    )
            except Exception as file_error:
                logger.error(f"使用文件對象失敗: {str(file_error)}")
                # 嘗試直接使用bytes和文件名
                response = await self.groq_client.audio.transcriptions.create(
                    file=("audio.wav", audio),
                    model="whisper-large-v3",
                    response_format="json",
                    language="en",
                    temperature=0.0
                )
            
            # 刪除臨時文件
            try:
                os.unlink(temp_file_path)
                logger.info("臨時音頻文件已刪除")
            except Exception as e:
                logger.warning(f"刪除臨時文件失敗: {str(e)}")
            
            logger.info(f"轉錄結果: {response.text}")
            return response.text
        except Exception as e:
            logger.error(f"語音轉文本過程中發生錯誤: {str(e)}")
            # 如果失敗，返回一個默認的回應
            return "無法識別語音，請重新嘗試。"
            
    async def groq_text_to_speech(self, message: str) -> bytes:
        """
        將文本轉換為音頻
        """
        try:
            response = await self.groq_client.audio.speech.create(
                model="playai-tts",
                voice="Fritz-PlayAI",
                input=message,
                response_format="wav"
            )
            # 確保我們正確處理協程對象
            audio_data = await response.read()
            logger.info(f"文本轉語音成功，生成了 {len(audio_data)} 字節的音頻")
            return audio_data
        except Exception as e:
            logger.error(f"文本轉語音失敗: {str(e)}")
            # 如果TTS失敗，返回一個簡單的提示音
            logger.info("生成一個簡單的提示音作為備選")
            try:
                # 生成一個簡單的提示音
                import wave
                import struct
                import math
                
                # 創建一個簡短的提示音
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_path = temp_file.name
                
                # 音頻參數
                duration = 1  # 秒
                sample_rate = 44100  # Hz
                frequency = 440  # Hz (A4音符)
                
                # 創建WAV文件
                with wave.open(temp_path, 'w') as wav_file:
                    wav_file.setnchannels(1)  # 單聲道
                    wav_file.setsampwidth(2)  # 2字節 = 16位
                    wav_file.setframerate(sample_rate)
                    
                    # 生成正弦波
                    for i in range(int(duration * sample_rate)):
                        value = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
                        data = struct.pack('<h', value)
                        wav_file.writeframes(data)
                
                # 讀取生成的WAV文件
                with open(temp_path, 'rb') as f:
                    audio_data = f.read()
                
                # 刪除臨時文件
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    logger.warning(f"刪除臨時文件失敗: {str(e)}")
                
                logger.info("成功生成提示音")
                return audio_data
            except Exception as e2:
                logger.error(f"生成提示音也失敗: {str(e2)}")
                raise ValueError(f"無法生成語音回應: {str(e)}")

    async def groq_voice_chat(self, audio: bytes, prompt: str, session_id: str) -> bytes:
        """
        處理語音對話，包括語音轉文本、生成回應和文本轉語音
        """
        if not self.is_online():
            raise ValueError("You need to be online for speech chat")
        
        logger.info(f"開始處理語音對話，會話ID: {session_id}")
        
        # 使用await調用異步函數
        try:
            voice_to_text: str = await self.groq_speech_to_text(audio=audio)
            logger.info(f"語音轉文本成功: '{voice_to_text}'")
            
            # Add user message to memory
            self.memory_manager.add_user_message(session_id, voice_to_text)
            
            # Get chat history
            chat_history = self.memory_manager.get_chat_history(session_id)
            logger.info(f"獲取聊天歷史，長度: {len(chat_history)}")
            
            # 收集完整回應
            full_response = ""
            logger.info("開始生成AI回應...")
            async for chunk in self.stream_groq_response_with_memory(
                prompt=prompt, user_query=voice_to_text, session_id=session_id):
                full_response += chunk
            
            logger.info(f"AI回應生成完成，長度: {len(full_response)}")
            
            # 將AI響應添加到記憶
            self.memory_manager.add_ai_message(session_id, full_response)
            
            # 使用await調用異步函數
            logger.info("開始將文本轉換為語音...")
            audio_response: bytes = await self.groq_text_to_speech(
                message=full_response)
            
            logger.info(f"語音對話處理完成，生成了 {len(audio_response)} 字節的音頻")
            return audio_response
        except Exception as e:
            logger.error(f"語音對話處理過程中發生錯誤: {str(e)}")
            # 返回一個簡單的錯誤提示音
            try:
                import wave
                import struct
                import math
                
                # 創建一個簡短的錯誤提示音
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_path = temp_file.name
                
                # 音頻參數 - 使用不同頻率表示錯誤
                duration = 0.5  # 秒
                sample_rate = 44100  # Hz
                frequency = 880  # Hz (A5音符，比正常提示音高一個八度)
                
                # 創建WAV文件
                with wave.open(temp_path, 'w') as wav_file:
                    wav_file.setnchannels(1)  # 單聲道
                    wav_file.setsampwidth(2)  # 2字節 = 16位
                    wav_file.setframerate(sample_rate)
                    
                    # 生成正弦波
                    for i in range(int(duration * sample_rate)):
                        value = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
                        data = struct.pack('<h', value)
                        wav_file.writeframes(data)
                
                # 讀取生成的WAV文件
                with open(temp_path, 'rb') as f:
                    audio_data = f.read()
                
                # 刪除臨時文件
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    logger.warning(f"刪除臨時文件失敗: {str(e)}")
                
                logger.info("成功生成錯誤提示音")
                return audio_data
            except Exception:
                # 如果連錯誤提示音都無法生成，則拋出原始異常
                raise

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
            #async for chunk in self.stream_local_npu_llama_response(prompt, user_query):
            async for chunk in self.mock_stream_ollama_response():
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
        
        prediction_stream = await self.groq_client.chat.completions.create(
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
