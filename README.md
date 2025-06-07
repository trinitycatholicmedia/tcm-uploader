# Trinity Catholic Media - Bible Verse to Pinterest Converter

A modular Streamlit application that extracts Malayalam Bible verses from images using AI and uploads them as Pinterest pins.

## 🏗️ Modular Architecture

The application has been refactored into a feature-oriented modular structure in the `uploader/` directory:

### 📁 Project Structure

```
uploader/
├── __init__.py              # Package initialization
├── config.py                # Configuration management
├── validators.py            # Input validation utilities
├── image_processor.py       # Image handling operations
├── ai_processor.py          # AI/Gemini integration
├── data_formatter.py        # Data processing and formatting
├── pinterest_api.py         # Pinterest API integration
├── ui_components.py         # Streamlit UI components
└── app_core.py             # Main application workflow
```

### 🎯 Feature Modules

#### `config.py`
- **Purpose**: Centralized configuration management
- **Features**:
  - Application constants and settings
  - Environment variable handling
  - UI configuration settings
  - Dataclass-based configuration objects

#### `validators.py`
- **Purpose**: Input validation and data verification
- **Features**:
  - API key validation
  - Pinterest credentials validation
  - Data integrity checks
  - Confidence level validation

#### `image_processor.py`
- **Purpose**: Image handling and processing
- **Features**:
  - Image loading and validation
  - File upload handling
  - Image metadata extraction
  - File size calculations

#### `ai_processor.py`
- **Purpose**: AI/Gemini integration for text extraction
- **Features**:
  - Gemini API configuration
  - Bible verse extraction prompts
  - AI response processing
  - GeminiProcessor class for encapsulation

#### `data_formatter.py`
- **Purpose**: Data processing and formatting
- **Features**:
  - JSON parsing and cleaning
  - Pinterest-specific data formatting
  - Text processing utilities
  - DataFormatter class for operations

#### `pinterest_api.py`
- **Purpose**: Pinterest API integration
- **Features**:
  - Pin upload functionality
  - API credential management
  - Error handling and validation
  - PinterestUploader class

#### `ui_components.py`
- **Purpose**: Streamlit UI component library
- **Features**:
  - Reusable UI components
  - Page configuration
  - Tab management
  - Form handling
  - Session state management

#### `app_core.py`
- **Purpose**: Main application workflow orchestration
- **Features**:
  - AppWorkflow class for coordination
  - Processing pipeline management
  - Error handling and recovery
  - State management

## 🚀 Usage

### Running the Application

```bash
# Using the new modular entry point
streamlit run main.py

# Or directly using the app core
streamlit run uploader/app_core.py
```

### Environment Variables

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
PINTEREST_ACCESS_TOKEN=your_pinterest_access_token_here
PINTEREST_BOARD_ID=your_pinterest_board_id_here
WHATSAPP_LINK=https://whatsapp.com/channel/0029VbAhLis0rGiVQd0HSw03
```

## 🔧 Development

### Adding New Features

1. **New Validation Rules**: Add to `validators.py`
2. **Image Processing**: Extend `image_processor.py`
3. **AI Functionality**: Modify `ai_processor.py`
4. **UI Components**: Add to `ui_components.py`
5. **Configuration**: Update `config.py`

### Testing Individual Modules

Each module can be imported and tested independently:

```python
from uploader.validators import validate_api_key
from uploader.image_processor import load_image
from uploader.ai_processor import GeminiProcessor
```

## 📊 Benefits of Modular Structure

### 🎯 **Separation of Concerns**
- Each module has a single, well-defined responsibility
- Easy to understand and maintain individual components
- Clear boundaries between different functionalities

### 🔧 **Maintainability**
- Changes to one feature don't affect others
- Easy to locate and fix bugs
- Simplified code reviews and updates

### 🧪 **Testability**
- Individual modules can be unit tested
- Mock dependencies for isolated testing
- Better test coverage and confidence

### 📈 **Scalability**
- Easy to add new features without breaking existing ones
- Modular components can be reused
- Team development with clear module ownership

### 🔄 **Reusability**
- Components can be used in other projects
- Common utilities are centralized
- Consistent patterns across the application

## 🛠️ Migration from Original Code

The original `streamlit.py` functionality has been preserved and enhanced:

- **✅ All original features maintained**
- **✅ Improved error handling**
- **✅ Better code organization**
- **✅ Enhanced maintainability**
- **✅ Cleaner architecture**

## 📋 Dependencies

The modular structure uses the same dependencies as the original:

```python
streamlit
google-generativeai
pillow
python-dotenv
requests
```

## 🎨 UI/UX Improvements

- Consistent component styling
- Better error message handling
- Improved user feedback
- Cleaner code organization for UI elements

---

## 🔍 Quick Start

1. **Install dependencies**:
   ```bash
   pip install streamlit google-generativeai pillow python-dotenv requests
   ```

2. **Set up environment variables** in `.env` file

3. **Run the application**:
   ```bash
   streamlit run main.py
   ```

4. **Upload a Malayalam Bible verse image**

5. **Review and edit the extracted data**

6. **Upload to Pinterest**

---

*This modular architecture makes the Trinity Catholic Media app more maintainable, testable, and scalable while preserving all original functionality.*
