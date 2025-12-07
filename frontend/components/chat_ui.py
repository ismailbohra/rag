"""
Chat UI Components
Renders messages, citations, and chat interface
"""
import streamlit as st
from typing import List, Dict, Optional


def render_message(role: str, content: str, citations: Optional[List[Dict]] = None):
    """Render a single chat message"""
    
    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)
    
    else:  # assistant
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(content)
            
            # Show citations if available
            if citations and st.session_state.get("show_citations", True):
                with st.expander("📎 Sources & Citations"):
                    render_citations(citations)


def render_citations(citations: List[Dict]):
    """Render citations with PDF links"""
    
    if not citations:
        st.info("No sources available")
        return
    
    for idx, citation in enumerate(citations, 1):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            source = citation.get("id", "Unknown")
            score = citation.get("score", 0)
            pdf_file = citation.get("pdf_file")
            
            st.markdown(f"**[{idx}] {source}** (Relevance: {score:.2%})")
            
            if pdf_file:
                st.caption(f"📄 File: `{pdf_file}`")
        
        with col2:
            if citation.get("pdf_link"):
                st.markdown(
                    f"[📥 Download]({citation['pdf_link']})",
                    help="Download the reference PDF"
                )


def render_chat_history(messages: List[Dict]):
    """Render all messages in chat history"""
    
    if not messages:
        st.info("No messages yet. Start by asking a question!")
        return
    
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        citations = msg.get("citations", [])
        
        render_message(role, content, citations if role == "assistant" else None)


def chat_input_area(placeholder: str = "Ask a question about the documents...") -> Optional[str]:
    """Get user input from chat box"""
    return st.chat_input(
        placeholder,
        key="user_input"
    )


def show_loading_message():
    """Show loading indicator while waiting for response"""
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("⏳ Thinking...")


def show_error_message(error: str):
    """Show error message"""
    st.error(f"❌ Error: {error}")


def show_success_message(message: str):
    """Show success message"""
    st.success(f"✅ {message}")
