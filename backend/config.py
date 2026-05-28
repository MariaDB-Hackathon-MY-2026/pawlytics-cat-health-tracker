"""
Configuration Management Module
Handles environment variables and application settings
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class"""
    
    # ==========================================
    # GEMINI API CONFIGURATION
    # ==========================================
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    GEMINI_RATE_LIMIT: int = int(os.getenv('GEMINI_RATE_LIMIT', '60'))
    
    # ==========================================
    # DATABASE CONFIGURATION
    # ==========================================
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
    DB_USER: str = os.getenv('DB_USER', 'root')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', 'kibble_db')
    DB_POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE', '5'))
    DB_MAX_OVERFLOW: int = int(os.getenv('DB_MAX_OVERFLOW', '10'))
    
    # ==========================================
    # APPLICATION SETTINGS
    # ==========================================
    APP_ENV: str = os.getenv('APP_ENV', 'development')
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # ==========================================
    # FILE UPLOAD SETTINGS
    # ==========================================
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv('MAX_UPLOAD_SIZE_MB', '10'))
    ALLOWED_EXTENSIONS: list = os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,webp').split(',')
    TEMP_UPLOAD_PATH: Path = Path(os.getenv('TEMP_UPLOAD_PATH', './temp_uploads'))
    
    # ==========================================
    # CACHING
    # ==========================================
    ENABLE_CACHE: bool = os.getenv('ENABLE_CACHE', 'True').lower() == 'true'
    CACHE_TTL_SECONDS: int = int(os.getenv('CACHE_TTL_SECONDS', '3600'))
    
    # ==========================================
    # LOGGING
    # ==========================================
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE_PATH: Path = Path(os.getenv('LOG_FILE_PATH', './logs/pawlytics.log'))
    
    # ==========================================
    # FEATURE FLAGS
    # ==========================================
    ENABLE_CAT_ANALYZER: bool = os.getenv('ENABLE_CAT_ANALYZER', 'True').lower() == 'true'
    ENABLE_BATCH_UPLOAD: bool = os.getenv('ENABLE_BATCH_UPLOAD', 'False').lower() == 'true'
    ENABLE_EXPORT_PDF: bool = os.getenv('ENABLE_EXPORT_PDF', 'False').lower() == 'true'
    
    # ==========================================
    # STREAMLIT CONFIGURATION
    # ==========================================
    STREAMLIT_SERVER_PORT: int = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
    STREAMLIT_SERVER_ADDRESS: str = os.getenv('STREAMLIT_SERVER_ADDRESS', 'localhost')
    STREAMLIT_THEME: str = os.getenv('STREAMLIT_THEME', 'light')
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate required configuration
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required API key
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is not set in environment variables")
        
        # Check database credentials
        if not cls.DB_PASSWORD:
            errors.append("DB_PASSWORD is not set (unsafe for production)")
        
        # Ensure upload directory exists
        if not cls.TEMP_UPLOAD_PATH.exists():
            try:
                cls.TEMP_UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create temp upload directory: {e}")
        
        # Ensure log directory exists
        if not cls.LOG_FILE_PATH.parent.exists():
            try:
                cls.LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create log directory: {e}")
        
        return (len(errors) == 0, errors)
    
    @classmethod
    def get_database_url(cls) -> str:
        """Generate database connection URL"""
        return f"mysql+mysqlconnector://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.APP_ENV.lower() == 'production'
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.APP_ENV.lower() == 'development'


# Validate configuration on import
is_valid, validation_errors = Config.validate()

if not is_valid:
    print("⚠️  Configuration Warnings:")
    for error in validation_errors:
        print(f"   - {error}")
    
    if Config.is_production():
        raise RuntimeError("Invalid configuration for production environment")
