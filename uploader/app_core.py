"""
Core application logic and workflow orchestration.
"""

import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any

from .config import get_env_config
from .image_processor import save_uploaded_file, validate_image_path
from .validators import validate_api_key
from .ai_processor import GeminiProcessor
from .data_formatter import parse_and_format_gemini_output
from .pinterest_api import PinterestUploader
from .ui_components import (
    setup_page_config, render_header, render_sidebar_config,
    render_file_upload, render_image_preview, render_process_button,
    render_results_tabs, render_upload_button, show_success_message,
    show_upload_progress, initialize_session_state, reset_session_state,
    render_privacy_policy_sidebar
)

class AppWorkflow:
    """Main application workflow orchestrator."""
    
    def __init__(self):
        """Initialize the application workflow."""
        load_dotenv()
        initialize_session_state()
        setup_page_config()
        
        # Load environment config
        self.env_config = get_env_config()
        
        # Initialize processors
        self.gemini_processor = None
        self.pinterest_uploader = None
    
    def setup_processors(self, config: Dict[str, str]) -> bool:
        """
        Set up AI and Pinterest processors with credentials.
        
        Args:
            config: Configuration dictionary from UI
            
        Returns:
            bool: True if processors are ready
        """
        # Set up Gemini processor
        api_key = config["api_key"] or self.env_config["gemini_api_key"]
        if api_key and validate_api_key(api_key):
            self.gemini_processor = GeminiProcessor(api_key)
            if not self.gemini_processor.is_ready():
                return False
        else:
            return False
        
        # Set up Pinterest uploader
        pinterest_token = config["pinterest_token"] or self.env_config["pinterest_access_token"]
        board_id = config["board_id"] or self.env_config["pinterest_board_id"]
        self.pinterest_uploader = PinterestUploader(pinterest_token, board_id)
        
        return True
    
    def process_image_workflow(self, uploaded_file, config: Dict[str, str]) -> bool:
        """
        Main image processing workflow.
        
        Args:
            uploaded_file: Streamlit uploaded file
            config: Configuration from UI
            
        Returns:
            bool: True if processing was successful
        """
        # Set up processors
        if not self.setup_processors(config):
            st.error("⚠️ Failed to initialize processors. Check your API credentials.")
            return False
        
        # Save uploaded file
        try:
            image_path = save_uploaded_file(uploaded_file)
            if not validate_image_path(image_path):
                return False
        except Exception as e:
            st.error(f"Error saving uploaded file: {e}")
            return False
        
        # Create progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Load and validate image
            status_text.text("🔄 Loading image...")
            progress_bar.progress(20)
            
            from PIL import Image
            image = Image.open(uploaded_file)
            
            # Step 2: Process with AI
            status_text.text("🤖 Extracting text with AI...")
            progress_bar.progress(40)
            
            raw_output = self.gemini_processor.extract_bible_verse(image)
            if not raw_output:
                st.error("Failed to extract text from image")
                return False
            
            # Step 3: Format data
            status_text.text("📝 Formatting extracted data...")
            progress_bar.progress(70)
            
            formatted_data = parse_and_format_gemini_output(raw_output)
            if not formatted_data:
                st.error("Failed to format extracted data")
                return False
            
            # Step 4: Save to session state
            status_text.text("✅ Processing complete!")
            progress_bar.progress(100)
            
            st.session_state.processed_data = formatted_data
            st.session_state.processing_complete = True
            st.session_state.current_image_path = str(image_path)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            st.success("🎉 Image processed successfully!")
            return True
            
        except Exception as e:
            st.error(f"Error during processing: {e}")
            progress_bar.empty()
            status_text.empty()
            return False
    
    def upload_to_pinterest_workflow(self, config: Dict[str, str]) -> bool:
        """
        Pinterest upload workflow.
        
        Args:
            config: Configuration from UI
            
        Returns:
            bool: True if upload was successful
        """
        if not st.session_state.processed_data:
            st.error("No processed data available for upload")
            return False
        
        # Update Pinterest uploader credentials
        pinterest_token = config["pinterest_token"] or self.env_config["pinterest_access_token"]
        board_id = config["board_id"] or self.env_config["pinterest_board_id"]
        
        if self.pinterest_uploader:
            self.pinterest_uploader.update_credentials(pinterest_token, board_id)
        else:
            self.pinterest_uploader = PinterestUploader(pinterest_token, board_id)
        
        # Get image path
        image_path = st.session_state.get('current_image_path', 'uploaded_image.jpg')
        
        # Upload to Pinterest
        with show_upload_progress():
            success = self.pinterest_uploader.upload_pin(
                image_path, 
                st.session_state.processed_data
            )
        
        if success:
            show_success_message()
            reset_session_state()
            return True
        
        return False
    
    def run(self):
        """Run the main application."""
        render_header()
        # Render sidebar and get config
        config = render_sidebar_config()
        render_privacy_policy_sidebar()
        
        # Main content layout
        col1, col2 = st.columns([1, 2], gap="large")
        
        with col1:
            # File upload section
            uploaded_file = render_file_upload()
            
            if uploaded_file:
                # Image preview
                from PIL import Image
                image = Image.open(uploaded_file)
                render_image_preview(image, uploaded_file)
                  # Process button
                if render_process_button():
                    if not validate_api_key(config["api_key"] or self.env_config["gemini_api_key"]):
                        st.error("⚠️ Please enter a valid Gemini API key.")
                    else:
                        self.process_image_workflow(uploaded_file, config)
        
        with col2:
            st.markdown("### 📊 Results")
            
            if not uploaded_file:
                st.info("📤 Upload an image to see results here.")
            elif st.session_state.processing_complete and st.session_state.processed_data:
                # Render results tabs
                upload_initiated = render_results_tabs(st.session_state.processed_data, config)
                
                # Handle upload if initiated
                if upload_initiated:
                    self.upload_to_pinterest_workflow(config)
            else:
                st.info("🔄 Process an image to see results here.")

def main():
    """Main entry point for the application."""
    app = AppWorkflow()
    app.run()

if __name__ == "__main__":
    main()
