"""
State Manager for Streamlit Session State
Initializes and manages user state across page reloads
"""
import streamlit as st
from typing import Optional


def init_session_state():
    """Initialize all session state variables"""
    
    # Authentication
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "token" not in st.session_state:
        st.session_state.token = None
    
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    
    # Session Management
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = None
    
    if "active_session_title" not in st.session_state:
        st.session_state.active_session_title = "New Chat"
    
    if "sessions_list" not in st.session_state:
        st.session_state.sessions_list = []
    
    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "show_citations" not in st.session_state:
        st.session_state.show_citations = True
    
    # UI State
    if "page" not in st.session_state:
        st.session_state.page = "chat"
    
    if "loading" not in st.session_state:
        st.session_state.loading = False


def set_logged_in(token: str, user_info: dict):
    """Set user as logged in"""
    st.session_state.logged_in = True
    st.session_state.token = token
    st.session_state.user_info = user_info


def logout():
    """Clear authentication and session state"""
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.user_info = None
    st.session_state.active_session_id = None
    st.session_state.messages = []


def set_active_session(session_id: Optional[str], title: str = "New Chat"):
    """Set the active chat session"""
    st.session_state.active_session_id = session_id
    st.session_state.active_session_title = title


def add_message(role: str, content: str, citations: list = None):
    """Add a message to chat history
    
    Args:
        role: "user" or "assistant"
        content: Message content/text
        citations: Optional list of citations for assistant messages
    """
    message = {
        "role": role,
        "content": content
    }
    
    # Add citations if provided (for assistant messages)
    if citations is not None:
        message["citations"] = citations
    
    st.session_state.messages.append(message)


def clear_messages():
    """Clear chat history for new session"""
    st.session_state.messages = []


def update_sessions_list(sessions: list):
    """Update the list of user's sessions"""
    st.session_state.sessions_list = sessions
