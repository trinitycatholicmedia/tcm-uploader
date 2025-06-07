"""
AI/Gemini integration module for text extraction from images.
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image
from typing import Optional
from .config import app_config

def configure_genai(api_key: str) -> None:
    """
    Configure Google Generative AI with the provided API key.
    
    Args:
        api_key: Google Gemini API key
    """
    genai.configure(api_key=api_key)

def get_gemini_model(model_name: str = None):
    """
    Get Gemini model instance.
    
    Args:
        model_name: Name of the model to use
        
    Returns:
        GenerativeModel instance or None if failed
    """
    if model_name is None:
        model_name = app_config.GEMINI_MODEL_NAME
        
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"Error: Could not load model '{model_name}'. Details: {e}")
        return None

def generate_gemini_content(model, prompt: str, image: Image.Image) -> Optional[str]:
    """
    Generate content using Gemini model.
    
    Args:
        model: Gemini model instance
        prompt: Text prompt for the model
        image: PIL Image object
        
    Returns:
        Generated text or None if failed
    """
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        st.error(f"Error during Gemini API call: {e}")
        return None

def get_bible_verse_extraction_prompt() -> str:
    """
    Get the prompt for extracting Bible verse information from images.
    
    Returns:
        str: The extraction prompt
    """
    return """
    Analyze this image and extract the following information as a JSON object:
    
    {
        "title": "The bible verse reference extracted from the image",
        "extracted_bible_verse_malayalam": "The Malayalam Bible verse text exactly as shown in the image",
        "bible_verse_english_translation": "English translation of the Malayalam verse",
        "alternative_text_for_main_content": "Alternative text describing what's in the image for accessibility",
        "confidence_level": "high/medium/low - your confidence in the extraction accuracy"
    }
    
    Important guidelines:
    - Extract the Malayalam text exactly as it appears
    - Provide accurate English translation
    - Be honest about confidence level
    - Make alt text descriptive for accessibility
    
    Return only the JSON object, no additional text.
    """

class GeminiProcessor:
    """Class to handle Gemini AI processing operations."""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini processor.
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        self.model = None
        self._configure()
    
    def _configure(self):
        """Configure Gemini with API key and load model."""
        configure_genai(self.api_key)
        self.model = get_gemini_model()
    
    def extract_bible_verse(self, image: Image.Image) -> Optional[str]:
        """
        Extract Bible verse information from image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text or None if failed
        """
        if not self.model:
            st.error("Gemini model not available")
            return None
        
        prompt = get_bible_verse_extraction_prompt()
        return generate_gemini_content(self.model, prompt, image)
    
    def is_ready(self) -> bool:
        """Check if the processor is ready to use."""
        return self.model is not None
