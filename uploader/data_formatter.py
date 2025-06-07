"""
Data formatting module for processing and formatting extracted data.
"""

import streamlit as st
import json
from typing import Dict, Any, Optional
from .config import DEFAULT_TITLE, DEFAULT_DESCRIPTION, WHATSAPP_LINK, REQUIRED_KEYS

def clean_json_string(json_str: str) -> str:
    """
    Clean JSON string by removing markdown formatting.
    
    Args:
        json_str: Raw JSON string
        
    Returns:
        Cleaned JSON string
    """
    cleaned = json_str.strip()
    for marker in ["```json", "```"]:
        if cleaned.startswith(marker):
            cleaned = cleaned[len(marker):]
        if cleaned.endswith(marker):
            cleaned = cleaned[:-len(marker)]
    cleaned = cleaned.strip()
    cleaned = cleaned.replace(",\n}", "\n}").replace(",\n]", "\n]")
    return cleaned

def parse_json_safely(json_str: str, original_str: str) -> Optional[Dict[str, Any]]:
    """
    Safely parse JSON string with error handling.
    
    Args:
        json_str: JSON string to parse
        original_str: Original string for error reporting
        
    Returns:
        Parsed dictionary or None if failed
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON: {e}\nRaw output was:\n{original_str}")
        return None

def ensure_required_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure all required fields are present in data.
    
    Args:
        data: Input data dictionary
        
    Returns:
        Dictionary with required fields
    """
    if not isinstance(data, dict):
        return {}
    return {key: data.get(key) for key in REQUIRED_KEYS}

def format_title(title: str) -> str:
    """
    Format title with branding.
    
    Args:
        title: Original title
        
    Returns:
        Formatted title
    """
    return f"{title.strip()} | Trinity Catholic Media" if title else DEFAULT_TITLE

def format_description(verse_malayalam: str, verse_english: str) -> str:
    """
    Format description with Malayalam verse, English translation, and WhatsApp link.
    
    Args:
        verse_malayalam: Malayalam verse text
        verse_english: English translation
        
    Returns:
        Formatted description
    """
    if not verse_malayalam or not verse_english:
        st.warning("Bible verse information is missing in the response.")
        return DEFAULT_DESCRIPTION
    return f"{verse_malayalam.strip()}\n\nEnglish: {verse_english.strip()}" + WHATSAPP_LINK

def format_alt_text(alt_text: str) -> str:
    """
    Format alternative text.
    
    Args:
        alt_text: Original alt text
        
    Returns:
        Formatted alt text
    """
    return alt_text.strip() if alt_text else ""

def parse_and_format_gemini_output(output_str: str) -> Dict[str, Any]:
    """
    Parse and format Gemini AI output into Pinterest-ready format.
    
    Args:
        output_str: Raw output from Gemini AI
        
    Returns:
        Formatted data dictionary
    """
    if not output_str:
        return {}
        
    cleaned_str = clean_json_string(output_str)
    parsed_data = parse_json_safely(cleaned_str, output_str)
    
    if not parsed_data:
        return {}
    
    data = ensure_required_fields(parsed_data)
    
    try:
        return {
            "title": format_title(data.get("title")),
            "description": format_description(
                data.get("extracted_bible_verse_malayalam"),
                data.get("bible_verse_english_translation")
            ),
            "alt_text": format_alt_text(data.get("alternative_text_for_main_content")),
            "confidence_level": data.get("confidence_level", "low").lower(),
        }
    except Exception as e:
        st.error(f"Error formatting output: {e}")
        return {}

def extract_verse_parts(description: str) -> Dict[str, str]:
    """
    Extract Malayalam and English parts from formatted description.
    
    Args:
        description: Formatted description string
        
    Returns:
        Dictionary with malayalam_text and english_text
    """
    result = {
        "malayalam_text": "Not extracted",
        "english_text": "Not available"
    }
    
    if not description:
        return result
    
    # Extract Malayalam part (before "English:")
    if 'English:' in description:
        result["malayalam_text"] = description.split('\n\nEnglish:')[0]
        # Extract English part (after "English:" but before WhatsApp link)
        english_part = description.split('English: ')[1].split('\n\n')[0]
        result["english_text"] = english_part
    
    return result

class DataFormatter:
    """Class to handle data formatting operations."""
    
    @staticmethod
    def format_pinterest_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw AI data for Pinterest upload.
        
        Args:
            raw_data: Raw data from AI processing
            
        Returns:
            Formatted data for Pinterest
        """
        return parse_and_format_gemini_output(json.dumps(raw_data) if isinstance(raw_data, dict) else str(raw_data))
    
    @staticmethod
    def validate_and_clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean data for consistency.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Cleaned and validated data
        """
        cleaned_data = {}
        
        # Clean and validate each field
        cleaned_data["title"] = data.get("title", "").strip()
        cleaned_data["description"] = data.get("description", "").strip()
        cleaned_data["alt_text"] = data.get("alt_text", "").strip()
        cleaned_data["confidence_level"] = data.get("confidence_level", "low").lower()
        
        return cleaned_data
