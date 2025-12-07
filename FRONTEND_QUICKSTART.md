# Quick Start Guide - RAG Chatbot Full Stack

## 🚀 Running the Complete Application

### Step 1: Start the Backend (FastAPI)

```bash
# Navigate to project root
cd d:\work\RAG

# Activate virtual environment
.venv\Scripts\activate

# Run the backend server
python -m uvicorn src.api.main:app --reload
```

✅ Backend running at: **http://localhost:8000**
📚 API docs at: **http://localhost:8000/docs**

### Step 2: Start the Frontend (Streamlit)

Open a new terminal:

```bash
# Navigate to frontend directory
cd d:\work\RAG\frontend

# Activate virtual environment (if not already)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

✅ Frontend running at: **http://localhost:8501**

## 📖 First Time Usage

### 1. Create an Account
- Go to **http://localhost:8501**
- Click **📝 Sign Up** tab
- Enter username, email, and password
- Click **✅ Sign Up**

### 2. Upload Documents
- Click **📤 Upload Documents** tab
- Drag and drop PDF files or click to select
- Click **🚀 Upload & Ingest**
- Wait for processing to complete

### 3. Start Chatting
- Click **💬 Chat** tab
- Type your question in the chat box
- Press Enter or click send
- View response with citations

### 4. Manage Sessions
- See all sessions in the left sidebar
- Click on any session to continue
- Click 🗑️ to delete a session
- Click ➕ New Chat for a new conversation

## 🎯 Key Features

| Feature | Access | Details |
|---------|--------|---------|
| **Login/Signup** | Auth screen | Email + password based |
| **Chat** | Chat tab | Multi-turn conversations |
| **Sessions** | Left sidebar | View all past conversations |
| **Upload** | Upload tab | Support multiple PDFs |
| **Citations** | Chat responses | Click "Sources & Citations" |
| **Settings** | Sidebar (bottom) | Toggle citations, adjust top_k |

## 📚 Example Queries

Try these after uploading documents:

1. **"What are the main topics covered?"**
2. **"Can you summarize the key points?"**
3. **"What does it say about [specific topic]?"**
4. **"Can you cite sources for that?"**
5. **"Tell me more about [previous topic]"** (conversation continuity)

## 🔧 Configuration

### Change Backend URL (if not on localhost)
Edit `frontend/app.py` line 23:
```python
BACKEND_URL = "http://your-api-server.com:8000"
```

### Adjust Document Retrieval Depth
In the sidebar, drag the **Documents to retrieve** slider:
- Lower (1-3): Faster, less context
- Higher (7-10): Slower, more context

## 🛠️ Troubleshooting

### "Failed to connect to backend"
- ✅ Ensure FastAPI is running on http://localhost:8000
- ✅ Check no firewalls blocking port 8000

### "Login failed: Invalid email or password"
- ✅ Make sure you created an account first
- ✅ Check email spelling and password

### "Upload failed"
- ✅ Files must be PDF format
- ✅ Check file size is reasonable
- ✅ Ensure `data/` folder exists and is writable

### "No response from query"
- ✅ Check backend is still running
- ✅ Ensure documents were uploaded first
- ✅ Review backend logs for errors

## 📊 Architecture Overview

```
┌─────────────────┐
│   Streamlit UI  │ (http://localhost:8501)
│   - Login       │
│   - Chat        │
│   - Upload      │
└────────┬────────┘
         │ HTTP Requests
         │ JWT Authorization
         ▼
┌──────────────────────┐
│   FastAPI Backend    │ (http://localhost:8000)
│   - Auth (JWT)       │
│   - Chat Sessions    │
│   - Query + RAG      │
│   - File Storage     │
└────────┬─────────────┘
         │ Database Queries
         ▼
┌──────────────────────┐
│   PostgreSQL + pgvector│
│   - Users            │
│   - Chat Sessions    │
│   - Chat Messages    │
│   - Embeddings       │
└──────────────────────┘
```

## 🔐 Security Notes

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens for API authentication
- ✅ Secure session management
- ✅ No passwords stored in frontend

## 📈 Next Steps

1. **Upload real documents** - Test with your own PDFs
2. **Test conversation flow** - Ask follow-up questions
3. **Review citations** - Check source references
4. **Manage sessions** - Create and organize multiple chats
5. **Deploy** - Move to production when ready

## 🚀 Production Deployment

### Backend
- Use Gunicorn instead of reload:
  ```bash
  gunicorn src.api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
  ```
- Set proper DATABASE_URL environment variable
- Use production-grade database

### Frontend
- Deploy to Streamlit Cloud or self-hosted
- Set BACKEND_URL to production URL
- Enable HTTPS

## 📞 Support

For issues:
1. Check backend logs: Terminal where uvicorn is running
2. Check frontend logs: Streamlit console output
3. Review browser console (F12) for JavaScript errors

---

**Happy chatting! 🤖✨**
