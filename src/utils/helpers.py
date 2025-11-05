"""
Helper Utilities.

This module contains utility functions used across the application.
"""

import re
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean and normalize text.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s\.\,\-]', '', text)

    return text.strip()


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from text.

    Args:
        text: Input text

    Returns:
        Email address if found, None otherwise
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from text.

    Args:
        text: Input text

    Returns:
        Phone number if found, None otherwise
    """
    # Simple phone pattern (can be enhanced)
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object to string.

    Args:
        dt: Datetime object
        format_str: Format string

    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def calculate_experience_years(start_date: datetime, end_date: Optional[datetime] = None) -> float:
    """
    Calculate years of experience.

    Args:
        start_date: Start date
        end_date: End date (defaults to now if None)

    Returns:
        Years of experience
    """
    if end_date is None:
        end_date = datetime.now()

    delta = end_date - start_date
    years = delta.days / 365.25

    return round(years, 1)


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate file extension.

    Args:
        filename: File name
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.docx'])

    Returns:
        True if extension is allowed
    """
    extension = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return extension in allowed_extensions
