"""
UI components module for Streamlit interface elements.
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple
from PIL import Image
from .config import ui_config
from .image_processor import get_image_info, calculate_file_size
from .data_formatter import extract_verse_parts
from .validators import validate_pinterest_data, validate_confidence_level

def setup_page_config():
    """Set up Streamlit page configuration."""
    st.set_page_config(
        page_title=ui_config.PAGE_TITLE,
        page_icon=ui_config.PAGE_ICON,
        layout=ui_config.LAYOUT,
        initial_sidebar_state=ui_config.SIDEBAR_STATE
    )

def render_header():
    """Render the main header section."""
    st.markdown("""
    <div class="main-header">
        <h1>📖 Trinity Catholic Media</h1>
        <h3>Bible Verse Image to Pinterest Pin Converter</h3>
        <p>Transform Malayalam Bible verse images into beautiful Pinterest pins</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_config() -> Dict[str, str]:
    """
    Render sidebar configuration section.
    
    Returns:
        dict: Configuration values from sidebar
    """
    with st.sidebar:
        st.markdown("### 🔑 Configuration")
        st.markdown("#### 🔐 API Credentials")
        
        api_key = st.text_input(
            "Gemini API Key", 
            value=st.session_state.get("gemini_api_key", ""), 
            type="password",
            help="Your Google Gemini API key for text extraction"
        )
        
        pinterest_token = st.text_input(
            "Pinterest Access Token", 
            value=st.session_state.get("pinterest_access_token", ""), 
            type="password",
            help="Your Pinterest API access token"
        )
        
        board_id = st.text_input(
            "Pinterest Board ID", 
            value=st.session_state.get("pinterest_board_id", ""),
            help="The ID of the Pinterest board to post to"
        )
    
    return {
        "api_key": api_key,
        "pinterest_token": pinterest_token,
        "board_id": board_id
    }

def render_file_upload() -> Optional[Any]:
    """
    Render file upload section.
    
    Returns:
        Uploaded file object or None
    """
    st.markdown("### 📁 Upload Image")
    return st.file_uploader(
        "Choose an image file",
        type=ui_config.SUPPORTED_IMAGE_TYPES,
        help="Upload an image containing Malayalam Bible verse text"
    )

def render_image_preview(image: Image.Image, uploaded_file: Any) -> None:
    """
    Render image preview with details.
    
    Args:
        image: PIL Image object
        uploaded_file: Streamlit uploaded file object
    """
    preview_col, info_col = st.columns([1, 1])
    
    with preview_col:
        st.markdown("### 🖼️ Preview")
        st.image(image, caption="Uploaded Image", width=ui_config.MAX_IMAGE_WIDTH_PREVIEW)
    
    with info_col:
        st.markdown("### ℹ️ Details")
        
        # Image info
        img_info = get_image_info(image)
        st.write(f"**Format:** {img_info['format']}")
        st.write(f"**Size:** {img_info['width']} x {img_info['height']}")
        
        # File size info
        size_info = calculate_file_size(uploaded_file)
        st.write(f"**File Size:** {size_info['formatted']}")

def render_process_button() -> bool:
    """
    Render the process button.
    
    Returns:
        bool: True if button was clicked
    """
    st.markdown("---")
    return st.button(
        "🚀 Process Image with AI", 
        key="main_process", 
        type="primary", 
        use_container_width=True
    )

def render_results_tabs(processed_data: Dict[str, Any], config: Dict[str, str] = None) -> bool:
    """
    Render results tabs with processed data.
    
    Args:
        processed_data: Processed data from AI
        config: Configuration from sidebar
        
    Returns:
        bool: True if upload was initiated
    """
    tab1, tab2, tab3 = st.tabs(["📝 Content", "🎯 Pinterest Data", "📋 Summary"])
    
    upload_initiated = False
    
    with tab1:
        render_content_tab(processed_data)
    
    with tab2:
        render_pinterest_data_tab(processed_data)
    
    with tab3:
        upload_initiated = render_summary_tab(processed_data, config)
    
    return upload_initiated

def render_content_tab(data: Dict[str, Any]) -> None:
    """
    Render content tab showing extracted text.
    
    Args:
        data: Processed data
    """
    subcol1, subcol2 = st.columns(2)
    
    # Extract verse parts
    verse_parts = extract_verse_parts(data.get('description', ''))
    
    with subcol1:
        st.markdown("**📖 Malayalam Verse:**")
        st.write(verse_parts["malayalam_text"])
        
    with subcol2:
        st.markdown("**🔤 English Translation:**")
        st.write(verse_parts["english_text"])
    
    st.markdown("**📄 Alt Text:**")
    st.write(data.get('alt_text', 'Not available'))

def render_pinterest_data_tab(data: Dict[str, Any]) -> None:
    """
    Render Pinterest data editing tab.
    
    Args:
        data: Processed data
    """
    st.markdown("### ✏️ Edit Pinterest Data")
    st.markdown("*You can modify the data below before uploading to Pinterest*")
    
    with st.form("pinterest_data_form"):
        st.markdown("#### 📝 Pinterest Pin Details")
        
        # Editable fields
        edited_title = st.text_input(
            "📋 Title:",
            value=data.get('title', ''),
            help="This will be the title of your Pinterest pin"
        )
        
        edited_description = st.text_area(
            "📄 Description:",
            value=data.get('description', ''),
            height=200,
            help="This will be the description of your Pinterest pin"
        )
        
        edited_alt_text = st.text_area(
            "🔍 Alt Text:",
            value=data.get('alt_text', ''),
            height=80,
            help="Alternative text for accessibility"
        )
        
        # Display confidence level
        confidence = data.get('confidence_level', 'low')
        st.markdown(f"**🎯 AI Confidence Level:** `{confidence.upper()}`")
        
        # Form buttons
        col1_form, col2_form = st.columns([1, 1])
        
        with col1_form:
            if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                # Update session state
                st.session_state.processed_data.update({
                    'title': edited_title,
                    'description': edited_description,
                    'alt_text': edited_alt_text
                })
                st.session_state.data_edited = True
                st.success("✅ Changes saved successfully!")
                st.rerun()
        
        with col2_form:
            if st.form_submit_button("🔄 Reset to Original", type="secondary", use_container_width=True):
                st.info("💡 To reset, please reprocess the image.")
    
    # Show raw JSON data
    with st.expander("🔍 View Raw JSON Data"):
        st.json(data)

def render_summary_tab(data: Dict[str, Any], config: Dict[str, str] = None) -> bool:
    """
    Render summary tab with validation and upload options.
    
    Args:
        data: Processed data
        config: Configuration from sidebar
        
    Returns:
        bool: True if upload was initiated
    """
    confidence = data.get("confidence_level", "low")
    
    st.markdown("### 📊 Upload Summary")
    
    # Data validation
    validation_results = validate_pinterest_data(data)
    
    col1_summary, col2_summary = st.columns([1, 1])
    
    with col1_summary:
        st.markdown("#### ✅ Data Validation")
        st.write(f"📋 Title: {'✅' if validation_results['title'] else '❌'} {'Valid' if validation_results['title'] else 'Missing/Empty'}")
        st.write(f"📄 Description: {'✅' if validation_results['description'] else '❌'} {'Valid' if validation_results['description'] else 'Missing/Empty'}")
        st.write(f"🔍 Alt Text: {'✅' if validation_results['alt_text'] else '❌'} {'Valid' if validation_results['alt_text'] else 'Missing/Empty'}")
    
    with col2_summary:
        st.markdown("#### 🎯 AI Analysis")
        if confidence == "high":
            st.success("🎯 High Confidence - Ready to upload!")
        elif confidence == "medium":
            st.warning("⚠️ Medium Confidence - Please review before uploading")
        else:
            st.error("❗ Low Confidence - Consider using a different image")
    
    # Instructions
    st.markdown("---")
    st.info("💡 **Tip:** You can edit the Pinterest data in the '🎯 Pinterest Data' tab before uploading.")
    
    # Upload button
    if config:
        button_clicked, upload_ready = render_upload_button(data, config)
        return button_clicked and upload_ready
    
    return False

def render_upload_button(data: Dict[str, Any], config: Dict[str, str]) -> Tuple[bool, bool]:
    """
    Render upload button with appropriate state.
    
    Args:
        data: Processed data
        config: Configuration from sidebar
        
    Returns:
        tuple: (button_clicked, upload_ready)
    """
    confidence = data.get("confidence_level", "low")
    validation_results = validate_pinterest_data(data)
    all_data_valid = all(validation_results.values())
    confidence_valid = validate_confidence_level(confidence)
    
    if confidence_valid and all_data_valid:
        button_clicked = st.button(
            "📌 Upload to Pinterest", 
            key="upload_pinterest", 
            type="primary", 
            use_container_width=True
        )
        
        if button_clicked and (not config["pinterest_token"] or not config["board_id"]):
            st.error("⚠️ Please enter Pinterest credentials in the sidebar.")
            return True, False
            
        return button_clicked, True
        
    elif not all_data_valid:
        st.error("❌ Upload disabled: Please ensure all Pinterest data fields are filled.")
        st.info("💡 Go to the '🎯 Pinterest Data' tab to complete missing information.")
        return False, False
        
    else:
        st.warning("⚠️ Upload disabled due to low confidence. Try with a clearer image or edit the data manually.")
        return False, False

def show_success_message():
    """Show success message after successful upload."""
    st.balloons()
    st.success("🎉 Successfully posted to Pinterest!")

def show_upload_progress():
    """Show upload progress spinner."""
    return st.spinner("📤 Uploading to Pinterest...")

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'data_edited' not in st.session_state:
        st.session_state.data_edited = False

def reset_session_state():
    """Reset session state after successful upload."""
    st.session_state.processed_data = None
    st.session_state.processing_complete = False
    st.session_state.data_edited = False