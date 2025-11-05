"""
Application settings and configuration.

This module loads environment variables and provides application-wide settings.
Supports both .env files (local) and Streamlit Cloud secrets.
"""

import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


def get_config(key: str, default: str = "") -> str:
    """
    Get configuration value from Streamlit secrets or environment variables.

    Priority:
    1. Streamlit Cloud secrets (st.secrets)
    2. Environment variables (os.getenv)
    3. Default value
    """
    # Try Streamlit secrets first (for Streamlit Cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return str(st.secrets[key])
    except (ImportError, FileNotFoundError, Exception):
        pass

    # Fall back to environment variables
    return os.getenv(key, default)


class Settings:
    """Application settings loaded from environment variables or Streamlit secrets."""

    # Application
    APP_NAME: str = get_config("APP_NAME", "AI Resume Screener")
    APP_VERSION: str = get_config("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = get_config("ENVIRONMENT", "development")
    DEBUG: bool = get_config("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = get_config("SECRET_KEY", "change-me-in-production")

    # API
    API_HOST: str = get_config("API_HOST", "0.0.0.0")
    API_PORT: int = int(get_config("API_PORT", "8000"))
    API_PREFIX: str = get_config("API_PREFIX", "/api/v1")

    # Database
    DATABASE_URL: str = get_config(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/resume_screening.db"
    )

    # AI/ML - Provider Selection
    AI_PROVIDER: str = get_config("AI_PROVIDER", "azure")  # azure, openai, or local

    # Azure OpenAI
    AZURE_OPENAI_ENABLED: bool = get_config("AZURE_OPENAI_ENABLED", "True").lower() == "true"
    AZURE_OPENAI_ENDPOINT: str = get_config("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = get_config("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_API_VERSION: str = get_config("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # Azure OpenAI - Embeddings
    AZURE_EMBEDDING_DEPLOYMENT: str = get_config("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
    AZURE_EMBEDDING_MODEL: str = get_config("AZURE_EMBEDDING_MODEL", "text-embedding-3-large")
    AZURE_EMBEDDING_DIMENSION: int = int(get_config("AZURE_EMBEDDING_DIMENSION", "3072"))

    # Azure OpenAI - GPT
    AZURE_GPT_DEPLOYMENT: str = get_config("AZURE_GPT_DEPLOYMENT", "gpt-4o-mini")
    AZURE_GPT_MODEL: str = get_config("AZURE_GPT_MODEL", "gpt-4o-mini")
    AZURE_GPT_API_VERSION: str = get_config("AZURE_GPT_API_VERSION", "2024-12-01-preview")

    # Local Models (Fallback)
    EMBEDDING_MODEL: str = get_config(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    VECTOR_DB_PATH: Path = Path(get_config("VECTOR_DB_PATH", f"{BASE_DIR}/data/vector_db"))
    VECTOR_DB_DIMENSION: int = int(get_config("VECTOR_DB_DIMENSION", "3072"))
    SPACY_MODEL: str = get_config("SPACY_MODEL", "en_core_web_sm")
    MIN_MATCH_SCORE: float = float(get_config("MIN_MATCH_SCORE", "0.5"))
    TOP_CANDIDATES_COUNT: int = int(get_config("TOP_CANDIDATES_COUNT", "10"))

    # Email
    SMTP_ENABLED: bool = get_config("SMTP_ENABLED", "True").lower() == "true"
    SMTP_HOST: str = get_config("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(get_config("SMTP_PORT", "587"))
    SMTP_USERNAME: str = get_config("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = get_config("SMTP_PASSWORD", "")
    EMAIL_FROM: str = get_config("EMAIL_FROM", "noreply@resumescreener.com")

    # Calendar
    GOOGLE_CALENDAR_ENABLED: bool = get_config("GOOGLE_CALENDAR_ENABLED", "False").lower() == "true"
    GOOGLE_CALENDAR_CREDENTIALS_PATH: str = get_config(
        "GOOGLE_CALENDAR_CREDENTIALS_PATH", "./credentials/google_calendar.json"
    )

    # Scheduler
    DEFAULT_INTERVIEW_DURATION: int = int(get_config("DEFAULT_INTERVIEW_DURATION", "60"))
    INTERVIEW_BUFFER_TIME: int = int(get_config("INTERVIEW_BUFFER_TIME", "15"))
    TIMEZONE: str = get_config("TIMEZONE", "Asia/Kolkata")

    # File Upload
    UPLOAD_DIR: Path = Path(get_config("UPLOAD_DIR", f"{BASE_DIR}/data/resumes"))
    MAX_FILE_SIZE_MB: int = int(get_config("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_EXTENSIONS: List[str] = get_config(
        "ALLOWED_EXTENSIONS", ".pdf,.doc,.docx"
    ).split(",")

    # Logging
    LOG_LEVEL: str = get_config("LOG_LEVEL", "INFO")
    LOG_FILE: str = get_config("LOG_FILE", f"{BASE_DIR}/logs/app.log")


# Create settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance."""
    return settings
