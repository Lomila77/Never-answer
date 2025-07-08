from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from typing import Dict, Any, Optional
import uuid

class MemoryManager:
    """Manages conversation memory for multiple users."""
    
    def __init__(self):
        # Dictionary to store conversation memory by session_id
        self.memories: Dict[str, ConversationBufferMemory] = {}
        
    def get_memory(self, session_id: Optional[str] = None) -> ConversationBufferMemory:
        """
        Get or create memory for a specific session.
        
        Args:
            session_id: The unique identifier for the session. If None, a new session is created.
            
        Returns:
            The conversation memory for the session.
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
            
        if session_id not in self.memories:
            message_history = ChatMessageHistory()
            self.memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                chat_memory=message_history,
                return_messages=True
            )
            
        return self.memories[session_id]
    
    def add_user_message(self, session_id: str, message: str) -> None:
        """
        Add a user message to the memory.
        
        Args:
            session_id: The session identifier.
            message: The user's message.
        """
        memory = self.get_memory(session_id)
        memory.chat_memory.add_user_message(message)
        
    def add_ai_message(self, session_id: str, message: str) -> None:
        """
        Add an AI message to the memory.
        
        Args:
            session_id: The session identifier.
            message: The AI's message.
        """
        memory = self.get_memory(session_id)
        memory.chat_memory.add_ai_message(message)
        
    def get_chat_history(self, session_id: str) -> str:
        """
        Get the conversation history as a formatted string.
        
        Args:
            session_id: The session identifier.
            
        Returns:
            The conversation history as a string.
        """
        memory = self.get_memory(session_id)
        return memory.buffer_as_str
    
    def clear_memory(self, session_id: str) -> None:
        """
        Clear the memory for a specific session.
        
        Args:
            session_id: The session identifier.
        """
        if session_id in self.memories:
            # Create a fresh ChatMessageHistory instance
            message_history = ChatMessageHistory()
            # Replace the existing memory with a new one
            self.memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                chat_memory=message_history,
                return_messages=True
            ) 