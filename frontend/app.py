"""
RAG Chatbot - Main Streamlit Application
Entry point for the frontend application
"""
import os
import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

# Import components (must be after path setup)
from api_client import APIClient
from state_manager import init_session_state, logout, set_active_session, clear_messages, add_message
from auth import auth_screen
from components import (
    render_chat_history,
    chat_input_area,
    show_loading_message,
    show_error_message,
    show_success_message,
    session_sidebar,
    document_upload
)


def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="RAG Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for styling
    st.markdown("""
    <style>
        /* Main content area */
        .main {
            padding: 1rem;
        }
        
        /* Chat messages styling */
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .user-message {
            background-color: #e3f2fd;
            margin-left: 2rem;
        }
        
        .assistant-message {
            background-color: #f5f5f5;
            margin-right: 2rem;
        }
        
        /* Sidebar styling */
        .sidebar-content {
            padding: 1rem 0;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
        }
        
        /* Header styling */
        .header {
            text-align: center;
            padding: 2rem 0;
        }
        
        /* Citation styling */
        .citation-box {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 0.5rem;
            margin-top: 0.5rem;
            border-radius: 0.25rem;
        }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application"""
    # Configure page first
    configure_page()
    
    # Initialize session state
    init_session_state()
    
    # Get backend URL from environment
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    api_client = APIClient(backend_url)
    
    # Set token if user is logged in
    if st.session_state.get("token"):
        api_client.set_token(st.session_state.token)
    
    # Check authentication
    if not st.session_state.get("logged_in"):
        # Show auth screen
        auth_screen(api_client)
        return
    
    # Render sidebar
    session_sidebar(api_client)
    
    # Header
    st.markdown(
        """
        <div class="header">
            <h1>🤖 RAG Chatbot</h1>
            <p>Ask questions about your documents</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Tabs for Chat and Upload
    tab1, tab2 = st.tabs(["💬 Chat", "📤 Documents"])
    
    with tab1:
        # Chat Interface
        st.markdown("### Chat")
        
        # Display chat history
        render_chat_history(st.session_state.get("messages", []))
        
        st.markdown("---")
        
        # Chat input
        user_input = chat_input_area("Type your question here...")
        
        if user_input:
            # Add user message to state immediately
            add_message("user", user_input)
            
            # Display user message immediately
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)
            
            # Get active session or create new one
            session_id = st.session_state.get("active_session_id")
            
            if not session_id:
                # Create new session
                try:
                    session_title = user_input[:50] + "..." if len(user_input) > 50 else user_input
                    session_data = api_client.create_session(session_title)
                    session_id = session_data.get("id")
                    set_active_session(session_id, session_title)
                except Exception as e:
                    st.error(f"❌ Failed to create session: {str(e)}")
                    st.stop()
            
            # Container for assistant response
            response_container = st.container()
            
            # Send query
            try:
                # Show loading state in container
                with response_container:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown("⏳ Thinking...")
                
                # Get settings from sidebar
                top_k = st.session_state.get("top_k", 5)
                
                # Send query to backend
                response = api_client.send_query(
                    query=user_input,
                    session_id=session_id,
                    top_k=top_k
                )
                
                # Extract response data from nested response structure
                response_data = response.get("response", {})
                answer = response_data.get("answer", "")
                citations = response_data.get("citations", [])
                
                # Add assistant message to state
                add_message("assistant", answer, citations)
                
                # Clear container and display actual response
                response_container.empty()
                with response_container:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(answer)
                        
                        # Show citations if enabled and available
                        if st.session_state.get("show_citations", True) and citations:
                            with st.expander("📚 Sources"):
                                st.markdown("**Retrieved Documents:**")
                                for i, citation in enumerate(citations, 1):
                                    col1, col2 = st.columns([3, 1])
                                    
                                    with col1:
                                        st.caption(
                                            f"{i}. {citation.get('source', 'Unknown')} "
                                            f"(Score: {citation.get('score', 0):.2f})"
                                        )
                                    
                                    with col2:
                                        if citation.get('pdf_file'):
                                            if st.button(
                                                "📥",
                                                key=f"download_{i}",
                                                help="Download PDF"
                                            ):
                                                try:
                                                    save_path = f".temp_downloads/{citation.get('pdf_file')}"
                                                    api_client.download_pdf(
                                                        citation.get('pdf_file'),
                                                        save_path
                                                    )
                                                    with open(save_path, "rb") as f:
                                                        st.download_button(
                                                            label="Download",
                                                            data=f.read(),
                                                            file_name=citation.get('pdf_file'),
                                                            mime="application/pdf"
                                                        )
                                                except Exception as e:
                                                    st.error(f"Error downloading: {str(e)}")
                
                st.success("✅ Response generated")
            
            except Exception as e:
                response_container.empty()
                with response_container:
                    st.error(f"❌ Error sending query: {str(e)}")
    
    with tab2:
        # Document upload interface
        document_upload(api_client)


if __name__ == "__main__":
    main()
