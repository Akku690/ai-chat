from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas import HealthResponse
from app.services import cache, ai_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    
    # Check database
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
    
    # Check Redis
    redis_ok = await cache.is_connected()
    
    # Check AI Service
    ai_ok = ai_service.client is not None
    
    return {
        "status": "healthy" if all([db_ok, redis_ok]) else "degraded",
        "database": db_ok,
        "redis": redis_ok,
        "ai_service": ai_ok
    }
