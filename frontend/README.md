# RAG Chatbot Frontend

A modern Streamlit-based frontend for the Retrieval-Augmented Generation (RAG) chatbot system.

## Features

- 🔐 JWT-based user authentication (login/signup)
- 💬 Chat interface with message history
- 📚 Document upload and indexing
- 🔍 Citation-based responses with PDF links
- 💾 Session management and history
- ⚙️ Customizable retrieval settings (top_k, citations toggle)
- 📥 PDF document download from citations

## Project Structure

```
frontend/
├── app.py                          # Main Streamlit application
├── api_client.py                   # API communication layer
├── state_manager.py                # Session state management
├── auth.py                         # Authentication UI
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── components/
    ├── __init__.py                 # Components module
    ├── chat_ui.py                  # Chat message rendering
    ├── session_sidebar.py          # Session management sidebar
    └── document_upload.py          # Document upload interface
```

## Installation

1. **Clone or navigate to the frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Create virtual environment (optional but recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```powershell
   cp .env.example .env
   # Edit .env with your backend URL
   ```

## Running the Application

```powershell
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Environment Variables

Create a `.env` file in the frontend directory:

```
BACKEND_URL=http://localhost:8000
```

- `BACKEND_URL`: URL of the backend API server (default: http://localhost:8000)

## Authentication Flow

1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Authenticate with email and password
3. **Session Token**: JWT token is stored and automatically sent with API requests
4. **Logout**: Clear token and return to login screen

## Features Overview

### Chat Interface
- Send questions about uploaded documents
- View response with relevant citations
- See document chunks with relevance scores
- Download source PDFs from citations

### Session Management
- Create new chat sessions
- View session history
- Delete old sessions
- Load previous conversations

### Document Upload
- Upload multiple PDF files
- Track processing progress
- Documents are automatically indexed
- Ready for RAG search immediately

### Settings
- **Show Citations**: Toggle citation display in responses
- **Top K Documents**: Select how many document chunks to retrieve (1-10)

## Components

### `api_client.py`
HTTP client for backend API communication:
- Authentication (signup, login, get current user)
- Session management (CRUD operations)
- Query processing with citations
- Document upload and download

### `state_manager.py`
Streamlit session state management:
- Authentication state (token, user info)
- Chat state (messages, active session)
- UI state (page, loading)
- Helper functions for state updates

### `auth.py`
User authentication interface:
- Login form with validation
- Sign-up form with password matching
- Dual-tab interface
- Error handling and user feedback

### `components/chat_ui.py`
Chat message rendering:
- User/assistant message display with avatars
- Citation display with source info
- Loading states and error messages
- Success notifications

### `components/session_sidebar.py`
Session management sidebar:
- User account info
- Session list with sorting
- Create/delete sessions
- Settings controls
- Logout button

### `components/document_upload.py`
Document upload interface:
- Multi-file selection
- Upload progress tracking
- File validation
- Success/error feedback

### `app.py`
Main application orchestration:
- Page configuration
- Authentication checks
- Tab-based interface (Chat/Documents)
- Message handling
- Integration of all components

## Error Handling

The application includes comprehensive error handling:
- Network error messages
- Authentication error feedback
- Validation error messages
- Graceful fallbacks for API failures

## Development

### Code Structure
- Modular component design for easy maintenance
- Type hints for better IDE support
- Consistent error handling patterns
- Documented functions and modules

### Adding Features
1. Add new API methods to `APIClient` class
2. Add state management to `state_manager.py`
3. Create UI components in `components/`
4. Integrate into `app.py`

## Troubleshooting

### "Connection refused" error
- Ensure backend API is running at the configured URL
- Check `BACKEND_URL` in `.env` file

### "Authentication failed"
- Verify email and password are correct
- Check that backend authentication is working

### "Document upload failed"
- Ensure PDF files are valid
- Check backend `/ingest/upload` endpoint is working
- Verify sufficient disk space on server

### Missing sessions or messages
- Try refreshing with the "Refresh" button in sidebar
- Check backend database connectivity
- Verify session API endpoints are responding

## Browser Compatibility

- Chrome/Chromium
- Firefox
- Safari
- Edge
- Any modern browser with WebSocket support

## Performance Tips

- Upload documents in batches (5-10 files at a time)
- Use reasonable top_k values (3-7 for faster responses)
- Clear old sessions periodically
- Monitor browser console for any warnings

## License

Same as main RAG project

## Support

For issues or questions about the frontend, check the main project README or backend documentation.
