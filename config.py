"""
ShadowRecon Configuration Module
Loads environment variables and API keys for OSINT operations
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration for ShadowRecon"""
    
    # API Keys (load from environment variables)
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
    HIBP_API_KEY = os.getenv("HIBP_API_KEY", "")
    
    # Feature flags
    ENABLE_SHODAN = os.getenv("ENABLE_SHODAN", "true").lower() == "true"
    ENABLE_VIRUSTOTAL = os.getenv("ENABLE_VIRUSTOTAL", "true").lower() == "true"
    ENABLE_HIBP = os.getenv("ENABLE_HIBP", "true").lower() == "true"
    
    # Timeout settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    ASYNC_TIMEOUT = int(os.getenv("ASYNC_TIMEOUT", "30"))
    
    # Username platforms to check
    USERNAME_PLATFORMS = {
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Reddit": "https://reddit.com/user/{}",
        "Instagram": "https://instagram.com/{}",
        "LinkedIn": "https://linkedin.com/in/{}",
        "YouTube": "https://youtube.com/@{}",
        "TikTok": "https://tiktok.com/@{}",
        "Medium": "https://medium.com/@{}",
        "DeviantArt": "https://deviantart.com/{}",
        "Twitch": "https://twitch.tv/{}",
    }
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = "shadowrecon.log"

def setup_logging():
    """Configure logging for the application"""
    logger = logging.getLogger("ShadowRecon")
    logger.setLevel(Config.LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOG_LEVEL)
    formatter = logging.Formatter(Config.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(Config.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Initialize logger
logger = setup_logging()
