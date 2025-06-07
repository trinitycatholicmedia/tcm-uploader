"""
Configuration module for the Trinity Catholic Media app.
Contains all constants, settings, and configuration classes.
"""

import os
from dataclasses import dataclass
from typing import List

# --- Constants ---
DEFAULT_TITLE = "Trinity Catholic Media"
DEFAULT_DESCRIPTION = (
    "Stay inspired daily! Follow our WhatsApp channel for the latest Bible verses: "
    "https://whatsapp.com/channel/0029VbAhLis0rGiVQd0HSw03"
)
WHATSAPP_LINK = (
    "\n\nStay inspired daily! Follow our WhatsApp channel for the latest Bible verses: "
    "https://whatsapp.com/channel/0029VbAhLis0rGiVQd0HSw03"
)
REQUIRED_KEYS = [
    "title",
    "extracted_bible_verse_malayalam",
    "bible_verse_english_translation",
    "alternative_text_for_main_content",
    "confidence_level",
]

@dataclass
class Config:
    """Application configuration settings."""
    DEFAULT_IMAGE_PATH: str = "tst.jpg"
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash-preview-05-20"
    DEFAULT_TAGS: List[str] = None
    
    def __post_init__(self):
        if self.DEFAULT_TAGS is None:
            self.DEFAULT_TAGS = ["bible quotes"]

@dataclass
class UIConfig:
    """UI-specific configuration settings."""
    PAGE_TITLE: str = "Trinity Catholic Media - Bible Verse to Pinterest"
    PAGE_ICON: str = "📖"
    LAYOUT: str = "wide"
    SIDEBAR_STATE: str = "expanded"
    
    # Upload settings
    SUPPORTED_IMAGE_TYPES: List[str] = None
    MAX_IMAGE_WIDTH_PREVIEW: int = 80
    
    def __post_init__(self):
        if self.SUPPORTED_IMAGE_TYPES is None:
            self.SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png"]

def get_env_config() -> dict:
    """Get environment-based configuration."""
    return {
        "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
        "pinterest_access_token": os.getenv("PINTEREST_ACCESS_TOKEN", ""),
        "pinterest_board_id": os.getenv("PINTEREST_BOARD_ID", ""),
        "whatsapp_link": os.getenv("WHATSAPP_LINK", "https://whatsapp.com/channel/0029VbAhLis0rGiVQd0HSw03")
    }

# Global instances
app_config = Config()
ui_config = UIConfig()
