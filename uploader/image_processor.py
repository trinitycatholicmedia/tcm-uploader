"""
Image processing module for handling image operations.
Includes validation, loading, and basic image utilities.
"""

import streamlit as st
from pathlib import Path
from PIL import Image
from typing import Optional

def validate_image_path(image_path: Path) -> bool:
    """
    Validate if the image path exists.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not image_path.exists():
        st.error(f"Image file not found at '{image_path}'")
        return False
    return True

def load_image(image_path: Path) -> Optional[Image.Image]:
    """
    Load an image from the given path.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        PIL Image object or None if failed
    """
    try:
        return Image.open(image_path)
    except Exception as e:
        st.error(f"Error opening image: {e}")
        return None

def save_uploaded_file(uploaded_file, filename: str = "uploaded_image.jpg") -> Path:
    """
    Save uploaded Streamlit file to disk.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        filename: Name to save the file as
        
    Returns:
        Path: Path to the saved file
    """
    image = Image.open(uploaded_file)
    image_path = Path(filename)
    image.save(image_path)
    return image_path

def get_image_info(image: Image.Image) -> dict:
    """
    Extract basic information about an image.
    
    Args:
        image: PIL Image object
        
    Returns:
        dict: Image information including format, size, etc.
    """
    return {
        "format": image.format,
        "size": image.size,
        "width": image.size[0],
        "height": image.size[1],
        "mode": image.mode
    }

def calculate_file_size(uploaded_file) -> dict:
    """
    Calculate file size information.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        dict: File size information
    """
    file_size_bytes = len(uploaded_file.getvalue())
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024
    
    return {
        "bytes": file_size_bytes,
        "kb": file_size_kb,
        "mb": file_size_mb,
        "formatted": f"{file_size_mb:.1f} MB" if file_size_mb > 1 else f"{file_size_kb:.1f} KB"
    }
