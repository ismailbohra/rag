# Frontend UI Wireframe & Component Guide

## 🎨 Screen Layouts

### 1. Authentication Screen

```
╔════════════════════════════════════════════════════════════╗
║                   🤖 RAG Chatbot                           ║
║     Intelligent Document Q&A with Citation Tracking       ║
╠════════════════════════════════════════════════════════════╣
║                                                             ║
║  ┌─────────────────────┐  ┌────────────────────────────┐  ║
║  │   [🔐 Login]        │  │    [📝 Sign Up]            │  ║
║  │   [Sign In Chosen]  │  │                            │  ║
║  │                     │  │                            │  ║
║  │ 📧 Email            │  │ 👤 Username                │  ║
║  │ [____________]      │  │ [____________]             │  ║
║  │                     │  │                            │  ║
║  │ 🔑 Password         │  │ 📧 Email                   │  ║
║  │ [____________]      │  │ [____________]             │  ║
║  │                     │  │                            │  ║
║  │ [🚀 Login]          │  │ 🔑 Password                │  ║
║  │                     │  │ [____________]             │  ║
║  │ ─────────────────   │  │                            │  ║
║  │ Don't have account? │  │ 🔑 Confirm                 │  ║
║  │ Switch to Sign Up→  │  │ [____________]             │  ║
║  │                     │  │                            │  ║
║  │       Features:     │  │ [✅ Sign Up]               │  ║
║  │ ✨ AI Q&A           │  │                            │  ║
║  │ 📚 Multi-docs       │  │ ─────────────────          │  ║
║  │ 💬 Sessions         │  │ Already have account?      │  ║
║  │ 📎 Citations        │  │ Switch to Login→           │  ║
║  │ 🔐 Secure           │  │                            │  ║
║  │                     │  │       Benefits:            │  ║
║  │                     │  │ ✅ Access docs             │  ║
║  │                     │  │ ✅ Save history            │  ║
║  │                     │  │ ✅ Personalized            │  ║
║  │                     │  │                            │  ║
║  └─────────────────────┘  └────────────────────────────┘  ║
║                                                             ║
║          Built with Streamlit + FastAPI | 2024             ║
╚════════════════════════════════════════════════════════════╝
```

### 2. Main Chat Screen

```
╔═════════════════════════════════════════════════════════════════╗
║                      🤖 RAG Chatbot                             ║
╠════════════════════╦═════════════════════════════════════════════╣
║   SIDEBAR          ║  CHAT CONTENT                               ║
║                    ║                                              ║
║ ─────────────────  ║  Session: New Chat                          ║
║ ### Account        ║  ─────────────────────────────────────────  ║
║ johndoe            ║                                              ║
║ john@email.com     ║  👤 User:                                    ║
║                    ║  What is RAG?                                ║
║ [🚪 Logout]        ║                                              ║
║                    ║  🤖 Assistant:                               ║
║ ─────────────────  ║  RAG (Retrieval-Augmented Generation)       ║
║ ### Sessions       ║  is a technique that combines...             ║
║                    ║                                              ║
║ [➕ New Chat]      ║  [📎 Sources & Citations] ▼                 ║
║ [🔄 Refresh]       ║                                              ║
║                    ║  [1] document.pdf (92%)                     ║
║ 💭 Last Convo      ║      📄 File: document.pdf                  ║
║    (2 hours ago)   ║      [📥 Download]                          ║
║ [  ] [🗑️]          ║                                              ║
║                    ║  👤 User:                                    ║
║ 💭 Project Notes   ║  Tell me more                                ║
║    (1 day ago)     ║                                              ║
║ [  ] [🗑️]          ║  🤖 Assistant:                               ║
║                    ║  ⏳ Thinking...                               ║
║ 💭 Documentation   ║                                              ║
║    (3 days ago)    ║  ─────────────────────────────────────────  ║
║ [  ] [🗑️]          ║                                              ║
║                    ║  [💬 Chat Input] 🔍 Ask something...        ║
║ ─────────────────  ║                                              ║
║ ### Settings       ║                                              ║
║                    ║                                              ║
║ ☑ Show citations   ║                                              ║
║                    ║                                              ║
║ Documents to       ║                                              ║
║ retrieve: [■■■─── ]║                                              ║
║            5 / 10   ║                                              ║
║                    ║                                              ║
║ RAG Chatbot v1.0   ║                                              ║
║ Powered by         ║                                              ║
║ FastAPI+Streamlit  ║                                              ║
╚════════════════════╩═════════════════════════════════════════════╝
```

### 3. Upload Documents Screen

```
╔═════════════════════════════════════════════════════════════════╗
║                    🤖 RAG Chatbot                               ║
║                 [💬 Chat] [📤 Upload Documents]                 ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ### 📤 Upload Documents                                        ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │                                                          │  ║
║  │  Drag and drop PDF files or click to select             │  ║
║  │                                                          │  ║
║  │         [📁 Choose PDF Files]                           │  ║
║  │                                                          │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║  **Selected 3 file(s):**                                        ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │ 📄 document1.pdf                      (245.3 KB) ✓       │  ║
║  │ 📄 research_paper.pdf                 (1.2 MB) ✓         │  ║
║  │ 📄 guidelines.pdf                     (450 KB) ✓         │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║  [🚀 Upload & Ingest]                                           ║
║                                                                  ║
║  ─────────────────────────────────────────────────────────────  ║
║                                                                  ║
║  ### 📊 Upload Results                                          ║
║                                                                  ║
║  ✅ Successfully uploaded 3 document(s)                         ║
║                                                                  ║
║  ✅ **document1.pdf**                                           ║
║     Path: `data/document1.pdf`                                 ║
║     Chunks indexed: 42                                         ║
║                                                                  ║
║  ✅ **research_paper.pdf**                                      ║
║     Path: `data/research_paper.pdf`                            ║
║     Chunks indexed: 67                                         ║
║                                                                  ║
║  ✅ **guidelines.pdf**                                          ║
║     Path: `data/guidelines.pdf`                                ║
║     Chunks indexed: 28                                         ║
║                                                                  ║
║  Total chunks: 137                                             ║
║                                                                  ║
╚═════════════════════════════════════════════════════════════════╝
```

### 4. Chat with Citations

```
╔═════════════════════════════════════════════════════════════════╗
║                    🤖 RAG Chatbot                               ║
║ Session: Documentation Review                                   ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  👤 User:                                                        ║
║  What are the main requirements for the project?                ║
║                                                                  ║
║                                                                  ║
║  🤖 Assistant:                                                   ║
║  According to the documentation, the main requirements are:     ║
║                                                                  ║
║  1. Python 3.8 or higher                                        ║
║  2. PostgreSQL database with pgvector extension                 ║
║  3. OpenAI or Gemini API key                                    ║
║  4. At least 2GB RAM for running the application                ║
║                                                                  ║
║  For detailed specifications, please refer to the installation  ║
║  guide in the documentation [1].                                ║
║                                                                  ║
║  ▼ [📎 Sources & Citations]                                     ║
║                                                                  ║
║  ┌───────────────────────────────────────────────────────────┐ ║
║  │ [1] guidelines.pdf (Relevance: 96%)                       │ ║
║  │     📄 File: `guidelines.pdf`                             │ ║
║  │                            [📥 Download]                  │ ║
║  │                                                           │ ║
║  │ [2] requirements.pdf (Relevance: 89%)                     │ ║
║  │     📄 File: `requirements.pdf`                           │ ║
║  │                            [📥 Download]                  │ ║
║  │                                                           │ ║
║  │ [3] setup_guide.pdf (Relevance: 85%)                      │ ║
║  │     📄 File: `setup_guide.pdf`                            │ ║
║  │                            [📥 Download]                  │ ║
║  └───────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║                                                                  ║
║  👤 User:                                                        ║
║  Can you explain more about the database requirements?          ║
║                                                                  ║
║                                                                  ║
║  🤖 Assistant:                                                   ║
║  ⏳ Thinking...                                                   ║
║                                                                  ║
║  ─────────────────────────────────────────────────────────────  ║
║                                                                  ║
║  [💬 Chat Input] 🔍 Ask a follow-up question...                ║
║                                                                  ║
╚═════════════════════════════════════════════════════════════════╝
```

## 🎯 Component Hierarchy

```
App (app.py)
│
├─ Sidebar (session_sidebar.py)
│  ├─ User Info Section
│  ├─ Session Management
│  │  ├─ New Chat Button
│  │  ├─ Session List
│  │  │  ├─ Session Button
│  │  │  └─ Delete Button
│  │  └─ Refresh Button
│  └─ Settings
│     ├─ Show Citations Toggle
│     └─ Top K Slider
│
├─ Main Content
│  │
│  ├─ Chat Tab
│  │  ├─ Session Title
│  │  ├─ Chat Messages (chat_ui.py)
│  │  │  ├─ User Message
│  │  │  ├─ Assistant Message
│  │  │  └─ Citations Expandable
│  │  │     └─ Citation List
│  │  │        └─ PDF Link
│  │  └─ Chat Input
│  │
│  └─ Upload Tab
│     └─ Document Upload (document_upload.py)
│        ├─ File Uploader
│        ├─ File List
│        ├─ Upload Button
│        └─ Results Display
│
└─ State Management (state_manager.py)
   ├─ Auth State
   ├─ Session State
   ├─ Messages State
   └─ UI State
```

## 🎨 Color Scheme & Typography

```
Colors:
- Primary: #FF6B35 (Orange - brand)
- Secondary: #004E89 (Blue - accent)
- Success: #2ecc71 (Green)
- Warning: #f39c12 (Amber)
- Error: #e74c3c (Red)
- Background: #f8f9fa (Light gray)
- Text: #2c3e50 (Dark gray)

Typography:
- Header: Bold, Large (24px+)
- Subheader: Bold, Medium (18px)
- Body: Regular (14px)
- Caption: Light, Small (12px)

Icons Used:
- 🤖 Bot/Assistant
- 👤 User
- 🔐 Login/Security
- 📝 Signup
- 💬 Chat/Conversation
- 📤 Upload
- 📎 Citations/Attachments
- 🔗 Links
- 📥 Download
- ➕ Add New
- 🗑️ Delete
- 🔄 Refresh
- ⚙️ Settings
- 🚀 Action/Launch
```

## 📱 Responsive Breakpoints

```
Desktop (>= 1024px)
├─ Sidebar: 300px width
├─ Main: Expanded
└─ Columns: 2+ supported

Tablet (768px - 1023px)
├─ Sidebar: Collapsible
├─ Main: 80% width
└─ Columns: 1.5

Mobile (< 768px)
├─ Sidebar: Bottom sheet
├─ Main: Full width
└─ Columns: 1 (stacked)
```

## 🔘 Interactive Elements

### Buttons
```
Primary: [🚀 Action Button]
Secondary: [ℹ️ Info Button]
Danger: [🗑️ Delete Button]
Link: [Link Text]
```

### Input Fields
```
Text: [____________]
Password: [•••••••••]
Slider: [■■■───]
Checkbox: ☑ Option
Dropdown: [Option ▼]
```

### Expandable Sections
```
▼ [Section Title] (expanded)
├─ Content...
└─ More content...

► [Section Title] (collapsed)
```

## 🎭 State Indicators

```
Loading: ⏳ Thinking...
Success: ✅ Success message
Warning: ⚠️ Warning message
Error: ❌ Error message
Info: ℹ️ Information
```

## 📊 Message Layout

```
User Message:
┌──────────────────────────────────────┐
│ 👤 User:                              │
│ Your message content here             │
└──────────────────────────────────────┘

Assistant Message:
┌──────────────────────────────────────┐
│ 🤖 Assistant:                         │
│ Response content here with multiple  │
│ lines and formatting support.        │
│                                      │
│ [📎 Sources & Citations] ▼           │
└──────────────────────────────────────┘

Citations:
┌──────────────────────────────────────┐
│ [1] document.pdf (Score: 92%)        │
│     📄 File: `document.pdf`          │
│                    [📥 Download]     │
│                                      │
│ [2] guide.pdf (Score: 85%)           │
│     📄 File: `guide.pdf`             │
│                    [📥 Download]     │
└──────────────────────────────────────┘
```

## ✨ Animation & Transitions

```
Page Load:
- Fade in components (0.3s)
- Slide in sidebar (0.4s)
- Fade in messages (0.2s per message)

Button Click:
- Brief highlight (0.1s)
- Scale animation (0.2s)

Loading State:
- Spinner animation (continuous)
- Pulse effect (1s interval)

Success/Error:
- Slide in toast (0.3s)
- Hold 2s
- Slide out (0.3s)
```

---

**This wireframe provides a complete visual guide for the Streamlit frontend implementation.**
