from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ConversationCreate, ConversationUpdate, ConversationResponse, ChatRequest, ChatResponse, MessageResponse
from app.services import ConversationService, MessageService, AnalyticsService, ai_service
from app.security import get_current_user
import time
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationResponse)
async def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new conversation"""
    conversation = await ConversationService.create_conversation(
        db=db,
        user_id=current_user.id,
        title=data.title
    )
    return conversation


@router.get("", response_model=list[ConversationResponse])
async def get_conversations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all user conversations"""
    conversations = await ConversationService.get_user_conversations(
        db=db,
        user_id=current_user.id
    )
    return conversations


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get specific conversation"""
    conversation = await ConversationService.get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation


@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update conversation title"""
    conversation = await ConversationService.update_conversation_title(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        title=data.title
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete conversation"""
    success = await ConversationService.delete_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return None


@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=100)
):
    """Get conversation messages"""
    conversation = await ConversationService.get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = await MessageService.get_conversation_messages(
        db=db,
        conversation_id=conversation_id
    )
    
    return messages[-limit:]


@router.post("/{conversation_id}/chat", response_model=ChatResponse)
async def send_message(
    conversation_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Send message and get AI response"""
    
    # Verify conversation exists
    conversation = await ConversationService.get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Store user message
    user_message = await MessageService.create_message(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        role="user",
        content=request.message
    )
    
    # Get conversation history
    messages = await MessageService.get_recent_messages(
        db=db,
        conversation_id=conversation_id,
        limit=10
    )
    
    # Prepare messages for AI
    chat_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in messages
    ]
    
    # Get AI response
    start_time = time.time()
    ai_response = await ai_service.get_response(
        messages=chat_messages,
        conversation_id=conversation_id
    )
    response_time_ms = (time.time() - start_time) * 1000
    
    # Store assistant message
    assistant_message = await MessageService.create_message(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        role="assistant",
        content=ai_response["content"],
        is_cached=ai_response.get("cached", False)
    )
    
    # Log analytics
    await AnalyticsService.log_event(
        db=db,
        user_id=current_user.id,
        event_type="message_sent",
        metadata={"conversation_id": conversation_id},
        response_time_ms=response_time_ms,
        tokens_used=ai_response.get("tokens_used")
    )
    
    return {
        "conversation_id": conversation_id,
        "user_message": user_message,
        "assistant_message": assistant_message,
        "tokens_used": ai_response.get("tokens_used"),
        "response_time_ms": response_time_ms
    }
