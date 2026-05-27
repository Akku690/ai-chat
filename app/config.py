from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Application
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    APP_NAME: str = "Smart Chat API with Memory"
    APP_VERSION: str = "1.0.0"

    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS & Hosts - JSON format from .env
    ALLOWED_HOSTS: List[str] = Field(default=["localhost", "127.0.0.1"])
    CORS_ORIGINS: List[str] = Field(default=["http://localhost", "http://localhost:8000"])
    FORCE_HTTPS: bool = False

    # Database (Render.com PostgreSQL)
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = 5432
    DB_USER: str = Field(default="chatuser")
    DB_PASSWORD: str = Field(default="chatpass")
    DB_NAME: str = Field(default="chatdb")

    @property
    def DATABASE_URL(self) -> str:
        """Construct PostgreSQL connection URL"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Redis (Render.com)
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = 6379
    REDIS_USER: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SSL: bool = False

    @property
    def REDIS_URL(self) -> str:
        """Construct Redis connection URL"""
        if self.REDIS_PASSWORD:
            return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # AI Services
    GEMINI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gemini-pro"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # Pydantic v2 Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
