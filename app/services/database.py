from sqlalchemy.orm import Session
from app.models import User, Conversation, Message, Analytics
from app.services.cache import cache
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    async def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    async def get_user_by_username(db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    async def get_user_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    async def create_user(db: Session, email: str, username: str, password: str) -> User:
        user = User(email=email, username=username)
        user.set_password(password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


class ConversationService:
    @staticmethod
    async def create_conversation(db: Session, user_id: int, title: str = "New Conversation") -> Conversation:
        conv = Conversation(user_id=user_id, title=title)
        db.add(conv)
        db.commit()
        db.refresh(conv)
        await cache.delete(f"conversations:user:{user_id}")
        return conv

    @staticmethod
    async def get_conversation(db: Session, conversation_id: int, user_id: int) -> Conversation:
        conv = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()
        return conv

    @staticmethod
    async def get_user_conversations(db: Session, user_id: int) -> list:
        cache_key = f"conversations:user:{user_id}"
        
        # Try cache first
        cached = await cache.get(cache_key)
        if cached:
            return cached

        # Fetch from DB
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).all()
        
        result = [c.to_dict() for c in conversations]
        
        # Cache for 1 hour
        await cache.set(cache_key, result, expire_seconds=3600)
        return result

    @staticmethod
    async def update_conversation_title(db: Session, conversation_id: int, user_id: int, title: str) -> Conversation:
        conv = await ConversationService.get_conversation(db, conversation_id, user_id)
        if conv:
            conv.title = title
            conv.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(conv)
            await cache.delete(f"conversations:user:{user_id}")
        return conv

    @staticmethod
    async def delete_conversation(db: Session, conversation_id: int, user_id: int) -> bool:
        conv = await ConversationService.get_conversation(db, conversation_id, user_id)
        if conv:
            db.query(Message).filter(Message.conversation_id == conversation_id).delete()
            db.delete(conv)
            db.commit()
            await cache.delete(f"conversations:user:{user_id}")
            return True
        return False


class MessageService:
    @staticmethod
    async def create_message(db: Session, conversation_id: int, user_id: int, role: str, content: str, is_cached: bool = False) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            is_cached=is_cached
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        await cache.delete(f"messages:conversation:{conversation_id}")
        return msg

    @staticmethod
    async def get_conversation_messages(db: Session, conversation_id: int) -> list:
        cache_key = f"messages:conversation:{conversation_id}"
        
        # Try cache first
        cached = await cache.get(cache_key)
        if cached:
            return cached

        # Fetch from DB
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        result = [m.to_dict() for m in messages]
        
        # Cache for 1 hour
        await cache.set(cache_key, result, expire_seconds=3600)
        return result

    @staticmethod
    async def get_recent_messages(db: Session, conversation_id: int, limit: int = 10) -> list:
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit).all()
        
        return [m.to_dict() for m in reversed(messages)]


class AnalyticsService:
    @staticmethod
    async def log_event(db: Session, user_id: int, event_type: str, 
                       metadata: dict = None, response_time_ms: float = None, 
                       tokens_used: int = None):
        analytics = Analytics(
            user_id=user_id,
            event_type=event_type,
            metadata=json.dumps(metadata or {}),
            response_time_ms=response_time_ms,
            tokens_used=tokens_used
        )
        db.add(analytics)
        db.commit()

    @staticmethod
    async def get_user_stats(db: Session, user_id: int, days: int = 30) -> dict:
        since = datetime.utcnow() - timedelta(days=days)
        
        events = db.query(Analytics).filter(
            Analytics.user_id == user_id,
            Analytics.created_at >= since
        ).all()

        total_messages = len([e for e in events if e.event_type == "message_sent"])
        total_tokens = sum([e.tokens_used for e in events if e.tokens_used])
        avg_response_time = sum([e.response_time_ms for e in events if e.response_time_ms]) / len([e for e in events if e.response_time_ms]) if events else 0

        return {
            "total_messages": total_messages,
            "total_tokens": total_tokens,
            "avg_response_time_ms": avg_response_time,
            "events_count": len(events),
        }
