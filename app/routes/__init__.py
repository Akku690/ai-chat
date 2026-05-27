from app.routes.auth import router as auth_router
from app.routes.conversations import router as conversations_router
from app.routes.analytics import router as analytics_router
from app.routes.health import router as health_router

__all__ = ["auth_router", "conversations_router", "analytics_router", "health_router"]
