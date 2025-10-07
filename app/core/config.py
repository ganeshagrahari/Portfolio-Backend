"""
Configuration management for the application
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    APP_NAME: str = "Ganesh's AI Assistant"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Backend
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # CORS
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,https://ganesh-portfolio-site.vercel.app"
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        # Add FRONTEND_URL if provided
        frontend_url = os.getenv("FRONTEND_URL", "").strip()
        if frontend_url and frontend_url not in origins:
            origins.append(frontend_url)
        return origins
    
    # RAG Settings
    VECTOR_STORE_PATH: str = "faiss_index"
    DATA_PATH: str = "data"
    CHUNK_SIZE: int = 1500  # Increased for better context
    CHUNK_OVERLAP: int = 200  # Increased overlap
    RETRIEVAL_K: int = 6  # Retrieve more documents for better answers
    
    # Session
    SESSION_TIMEOUT: int = 3600  # 1 hour in seconds
    
    class Config:
        case_sensitive = True


# Create settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
