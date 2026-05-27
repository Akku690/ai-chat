from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AnalyticsResponse
from app.services import AnalyticsService
from app.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/stats", response_model=AnalyticsResponse)
async def get_user_stats(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get user analytics and stats"""
    stats = await AnalyticsService.get_user_stats(
        db=db,
        user_id=current_user.id,
        days=days
    )
    return stats
