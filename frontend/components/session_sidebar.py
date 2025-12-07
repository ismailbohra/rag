"""
Session Sidebar Component
Manages chat sessions and navigation
"""
import streamlit as st
from api_client import APIClient
from state_manager import set_active_session, clear_messages, update_sessions_list
from typing import Optional


def session_sidebar(api_client: APIClient):
    """Sidebar for session management"""
    
    with st.sidebar:
        # User Info
        st.markdown("---")
        st.markdown("### 👤 Account")
        if st.session_state.user_info:
            user = st.session_state.user_info
            st.write(f"**{user.get('username', 'User')}**")
            st.caption(user.get('email', 'no-email'))
        
        if st.button("🚪 Logout", use_container_width=True):
            from state_manager import logout
            logout()
            st.rerun()
        
        st.markdown("---")
        
        # Session Management
        st.markdown("### 💬 Chat Sessions")
        
        # New Session Button
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ New Chat", use_container_width=True):
                set_active_session(None, "New Chat")
                clear_messages()
                st.rerun()
        
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                try:
                    sessions = api_client.get_sessions()
                    update_sessions_list(sessions)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error refreshing: {str(e)}")
        
        st.markdown("---")
        
        # Sessions List
        try:
            sessions = st.session_state.get("sessions_list", [])
            
            if not sessions:
                st.info("No saved sessions yet")
            else:
                st.markdown("**Your Sessions:**")
                
                # Sort by last activity
                sessions_sorted = sorted(
                    sessions,
                    key=lambda x: x.get("last_activity", ""),
                    reverse=True
                )
                
                for session in sessions_sorted:
                    session_id = session.get("id")
                    title = session.get("title", "Untitled")
                    last_activity = session.get("last_activity", "")
                    
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        if st.button(
                            f"💭 {title}",
                            key=f"session_{session_id}",
                            use_container_width=True
                        ):
                            try:
                                # Load session messages
                                messages = api_client.get_session_messages(session_id)
                                set_active_session(session_id, title)
                                st.session_state.messages = messages
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error loading session: {str(e)}")
                    
                    with col2:
                        if st.button(
                            "🗑️",
                            key=f"delete_{session_id}",
                            help="Delete this session"
                        ):
                            try:
                                api_client.delete_session(session_id)
                                sessions = api_client.get_sessions()
                                update_sessions_list(sessions)
                                
                                if st.session_state.active_session_id == session_id:
                                    set_active_session(None)
                                    clear_messages()
                                
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting: {str(e)}")
        
        except Exception as e:
            st.error(f"Error loading sessions: {str(e)}")
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        
        show_citations = st.checkbox(
            "Show citations",
            value=st.session_state.get("show_citations", True),
            key="show_citations_checkbox"
        )
        st.session_state.show_citations = show_citations
        
        top_k = st.slider(
            "Documents to retrieve:",
            min_value=1,
            max_value=10,
            value=5,
            key="top_k_slider"
        )
        st.session_state.top_k = top_k
        
        st.markdown("---")
        
        # Footer
        st.markdown(
            """
            <div style="text-align: center; color: gray; font-size: 0.8em; margin-top: 2rem;">
                RAG Chatbot v1.0<br>
                Powered by FastAPI + Streamlit
            </div>
            """,
            unsafe_allow_html=True
        )
