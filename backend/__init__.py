"""
Pawlytics Backend Package
"""

from .config import Config
from .database import Database, db_instance
from .gemini_service import GeminiAnalyzer
from .models import (
    KibbleCreate,
    KibbleResponse,
    CatCreate,
    CatResponse,
    FeedingLogCreate,
    FeedingLogResponse,
    validate_kibble_data,
    validate_cat_data
)

__version__ = "1.0.0"
__all__ = [
    "Config",
    "Database",
    "db_instance",
    "GeminiAnalyzer",
    "KibbleCreate",
    "KibbleResponse",
    "CatCreate",
    "CatResponse",
    "FeedingLogCreate",
    "FeedingLogResponse",
    "validate_kibble_data",
    "validate_cat_data",
]
