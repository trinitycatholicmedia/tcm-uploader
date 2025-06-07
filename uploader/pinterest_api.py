"""
Pinterest API integration module for uploading pins.
"""

import streamlit as st
import requests
import json
import base64
import os
from typing import Dict, Any, Optional
from .config import get_env_config

def upload_to_pinterest(image_path: str, formatted_data: Dict[str, Any], access_token: str, board_id: str) -> bool:
    """
    Upload an image as a pin to Pinterest.
    
    Args:
        image_path: Path to the image file
        formatted_data: Formatted data for Pinterest
        access_token: Pinterest access token
        board_id: Pinterest board ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    required_fields = ["title", "description", "alt_text"]
    if not all(formatted_data.get(field) for field in required_fields):
        st.error("Missing required fields for Pinterest upload")
        return False
    
    # Get WhatsApp link from environment or use default
    env_config = get_env_config()
    link = env_config["whatsapp_link"]
    
    # Convert image to base64
    try:
        with open(image_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        st.error(f"Error reading image for base64 upload: {e}")
        return False
    
    # Prepare headers and payload
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    
    payload = {
        'board_id': board_id,
        'media_source': {
            'source_type': 'image_base64',
            'content_type': 'image/jpeg',
            'data': image_base64,
        },
        'title': formatted_data["title"],
        'description': formatted_data["description"],
        'link': link,
        'alt_text': formatted_data["alt_text"],
    }
    
    # Make API request
    try:
        response = requests.post(
            'https://api.pinterest.com/v5/pins',
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.ok:
            st.success('Pin created successfully!')
            st.json(response.json())
            return True
        else:
            st.error(f'Failed to create pin: {response.status_code} {response.text}')
            return False
            
    except Exception as e:
        st.error(f"Pinterest upload error: {str(e)}")
        return False

class PinterestUploader:
    """Class to handle Pinterest upload operations."""
    
    def __init__(self, access_token: str = None, board_id: str = None):
        """
        Initialize Pinterest uploader.
        
        Args:
            access_token: Pinterest access token
            board_id: Pinterest board ID
        """
        env_config = get_env_config()
        self.access_token = access_token or env_config["pinterest_access_token"]
        self.board_id = board_id or env_config["pinterest_board_id"]
    
    def is_configured(self) -> bool:
        """Check if Pinterest credentials are configured."""
        return bool(self.access_token and self.board_id)
    
    def upload_pin(self, image_path: str, data: Dict[str, Any]) -> bool:
        """
        Upload a pin to Pinterest.
        
        Args:
            image_path: Path to the image file
            data: Pin data (title, description, alt_text)
            
        Returns:
            bool: True if successful
        """
        if not self.is_configured():
            st.error("Pinterest credentials not configured")
            return False
        
        return upload_to_pinterest(image_path, data, self.access_token, self.board_id)
    
    def validate_pin_data(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate pin data for upload.
        
        Args:
            data: Pin data to validate
            
        Returns:
            dict: Validation results with error messages
        """
        errors = {}
        
        required_fields = {
            "title": "Pin title is required",
            "description": "Pin description is required", 
            "alt_text": "Alt text is required for accessibility"
        }
        
        for field, error_msg in required_fields.items():
            if not data.get(field, "").strip():
                errors[field] = error_msg
        
        return errors
    
    def update_credentials(self, access_token: str, board_id: str):
        """
        Update Pinterest credentials.
        
        Args:
            access_token: New access token
            board_id: New board ID
        """
        self.access_token = access_token
        self.board_id = board_id
