import logging
import asyncio
from app.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """AI Service using Gemini"""
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.AI_MODEL
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Gemini client"""
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model)
                logger.info(f"Gemini client initialized with model: {self.model}")
            except ImportError:
                logger.warning("google-generativeai not installed.")
            except Exception as e:
                logger.error(f"Gemini init error: {e}")
        else:
            logger.warning("GEMINI_API_KEY not configured. Using mock responses.")

    async def get_response(self, messages: list, conversation_id: int) -> dict:
        """Get Gemini response for conversation"""
        try:
            if not self.client:
                return {
                    "content": "Mock response. Configure GEMINI_API_KEY to use Gemini.",
                    "tokens_used": 0,
                    "model": self.model,
                    "cached": False,
                }

            # Convert messages to Gemini format
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

            response = await asyncio.to_thread(
                self.client.generate_content, prompt
            )

            return {
                "content": response.text,
                "tokens_used": 0,
                "model": self.model,
                "cached": False,
            }
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return {
                "content": f"Error: {str(e)}",
                "tokens_used": 0,
                "model": self.model,
                "cached": False,
                "error": True,
            }

    async def validate_conversation(self, messages: list) -> bool:
        if not isinstance(messages, list):
            return False
        for msg in messages:
            if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                return False
        return True

ai_service = AIService()
