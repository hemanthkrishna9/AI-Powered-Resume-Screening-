"""
Application settings and configuration.

This module loads environment variables and provides application-wide settings.
"""

import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = os.getenv("APP_NAME", "AI Resume Screener")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/resume_screening.db"
    )

    # AI/ML - Provider Selection
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "azure")  # azure, openai, or local

    # Azure OpenAI
    AZURE_OPENAI_ENABLED: bool = os.getenv("AZURE_OPENAI_ENABLED", "True").lower() == "true"
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    # Azure OpenAI - Embeddings
    AZURE_EMBEDDING_DEPLOYMENT: str = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
    AZURE_EMBEDDING_MODEL: str = os.getenv("AZURE_EMBEDDING_MODEL", "text-embedding-3-large")
    AZURE_EMBEDDING_DIMENSION: int = int(os.getenv("AZURE_EMBEDDING_DIMENSION", "3072"))

    # Azure OpenAI - GPT
    AZURE_GPT_DEPLOYMENT: str = os.getenv("AZURE_GPT_DEPLOYMENT", "gpt-4o-mini")
    AZURE_GPT_MODEL: str = os.getenv("AZURE_GPT_MODEL", "gpt-4o-mini")
    AZURE_GPT_API_VERSION: str = os.getenv("AZURE_GPT_API_VERSION", "2024-12-01-preview")

    # Local Models (Fallback)
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    VECTOR_DB_PATH: Path = Path(os.getenv("VECTOR_DB_PATH", f"{BASE_DIR}/data/vector_db"))
    VECTOR_DB_DIMENSION: int = int(os.getenv("VECTOR_DB_DIMENSION", "3072"))
    SPACY_MODEL: str = os.getenv("SPACY_MODEL", "en_core_web_sm")
    MIN_MATCH_SCORE: float = float(os.getenv("MIN_MATCH_SCORE", "0.5"))
    TOP_CANDIDATES_COUNT: int = int(os.getenv("TOP_CANDIDATES_COUNT", "10"))

    # Email
    SMTP_ENABLED: bool = os.getenv("SMTP_ENABLED", "True").lower() == "true"
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@resumescreener.com")

    # Calendar
    GOOGLE_CALENDAR_ENABLED: bool = os.getenv("GOOGLE_CALENDAR_ENABLED", "False").lower() == "true"
    GOOGLE_CALENDAR_CREDENTIALS_PATH: str = os.getenv(
        "GOOGLE_CALENDAR_CREDENTIALS_PATH", "./credentials/google_calendar.json"
    )

    # Scheduler
    DEFAULT_INTERVIEW_DURATION: int = int(os.getenv("DEFAULT_INTERVIEW_DURATION", "60"))
    INTERVIEW_BUFFER_TIME: int = int(os.getenv("INTERVIEW_BUFFER_TIME", "15"))
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata")

    # File Upload
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", f"{BASE_DIR}/data/resumes"))
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_EXTENSIONS: List[str] = os.getenv(
        "ALLOWED_EXTENSIONS", ".pdf,.doc,.docx"
    ).split(",")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", f"{BASE_DIR}/logs/app.log")


# Create settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance."""
    return settings
