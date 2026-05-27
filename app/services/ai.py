import logging
import asyncio
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """AI Service for chat completions"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize OpenAI client"""
        if self.api_key:
            try:
                import openai
                openai.api_key = self.api_key
                self.client = openai
                logger.info(f"OpenAI client initialized with model: {self.model}")
            except ImportError:
                logger.warning("OpenAI library not installed. Using mock responses.")
        else:
            logger.warning("OPENAI_API_KEY not configured. Using mock responses.")

    async def get_response(self, messages: list, conversation_id: int) -> dict:
        """
        Get AI response for conversation
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            conversation_id: ID of conversation for logging
            
        Returns:
            Dict with 'content', 'tokens_used', 'model', 'cached'
        """
        try:
            if not self.client:
                # Mock response for development
                return {
                    "content": "This is a mock response. Configure OPENAI_API_KEY to use real AI.",
                    "tokens_used": 0,
                    "model": self.model,
                    "cached": False,
                }

            # Real OpenAI call
            response = await asyncio.to_thread(
                self.client.ChatCompletion.create,
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "model": self.model,
                "cached": False,
            }

        except Exception as e:
            logger.error(f"AI service error: {e}")
            return {
                "content": f"Error generating response: {str(e)}",
                "tokens_used": 0,
                "model": self.model,
                "cached": False,
                "error": True,
            }

    async def validate_conversation(self, messages: list) -> bool:
        """Validate conversation format"""
        if not isinstance(messages, list):
            return False
        for msg in messages:
            if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                return False
        return True


ai_service = AIService()
