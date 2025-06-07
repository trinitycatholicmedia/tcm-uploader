"""
Validation module for various input validations.
"""

import streamlit as st
from pathlib import Path
from typing import Dict, Any

def validate_api_key(api_key: str) -> bool:
    """
    Validate if API key is provided.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not api_key:
        st.error("GEMINI_API_KEY is required.")
        return False
    return True

def validate_pinterest_credentials(pinterest_token: str, board_id: str) -> bool:
    """
    Validate Pinterest credentials.
    
    Args:
        pinterest_token: Pinterest access token
        board_id: Pinterest board ID
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not pinterest_token:
        st.error("Pinterest Access Token is required.")
        return False
    if not board_id:
        st.error("Pinterest Board ID is required.")
        return False
    return True

def validate_pinterest_data(data: Dict[str, Any]) -> Dict[str, bool]:
    """
    Validate Pinterest upload data.
    
    Args:
        data: Dictionary containing Pinterest data
        
    Returns:
        dict: Validation results for each field
    """
    required_fields = ["title", "description", "alt_text"]
    validation_results = {}
    
    for field in required_fields:
        validation_results[field] = bool(data.get(field, '').strip())
    
    return validation_results

def validate_all_pinterest_data(data: Dict[str, Any]) -> bool:
    """
    Check if all Pinterest data is valid.
    
    Args:
        data: Dictionary containing Pinterest data
        
    Returns:
        bool: True if all data is valid
    """
    validation_results = validate_pinterest_data(data)
    return all(validation_results.values())

def validate_confidence_level(confidence: str) -> bool:
    """
    Validate if confidence level is acceptable for upload.
    
    Args:
        confidence: Confidence level string
        
    Returns:
        bool: True if acceptable for upload
    """
    return confidence.lower() in ["high", "medium"]
