"""
Login & Signup Authentication UI Components
"""
import streamlit as st
import requests
from api_client import APIClient
from state_manager import set_logged_in


def login_screen(api_client: APIClient):
    """Login form UI"""
    st.title("🔐 Login")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Sign In to Your Account")
        
        email = st.text_input(
            "📧 Email",
            placeholder="your@email.com",
            key="login_email"
        )
        
        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="••••••••",
            key="login_password"
        )
        
        if st.button("🚀 Login", use_container_width=True, type="primary"):
            if not email or not password:
                st.error("Please enter email and password")
                return
            
            try:
                with st.spinner("Logging in..."):
                    result = api_client.login(email, password)
                    token = result.get("access_token")
                    
                    if token:
                        api_client.set_token(token)
                        user_info = api_client.get_current_user()
                        set_logged_in(token, user_info)
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Login failed: No token received")
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    st.error("❌ Invalid email or password")
                else:
                    st.error(f"❌ Login error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
        
        st.markdown("---")
        st.markdown("Don't have an account? Switch to **Sign Up** →")
    
    with col2:
        st.markdown("### Features")
        st.markdown("""
        ✨ **RAG Chatbot Features:**
        
        - 🤖 AI-powered Q&A
        - 📚 Multi-document retrieval
        - 💬 Persistent chat sessions
        - 📎 Citation tracking
        - 🔐 Secure authentication
        
        **Privacy:** Your data is encrypted and secure.
        """)


def signup_form(api_client: APIClient):
    """Signup form UI"""
    st.title("📝 Create Account")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Sign Up for Free")
        
        username = st.text_input(
            "👤 Username",
            placeholder="your_username",
            key="signup_username"
        )
        
        email = st.text_input(
            "📧 Email",
            placeholder="your@email.com",
            key="signup_email"
        )
        
        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="••••••••",
            key="signup_password"
        )
        
        confirm_password = st.text_input(
            "🔑 Confirm Password",
            type="password",
            placeholder="••••••••",
            key="signup_confirm"
        )
        
        if st.button("✅ Sign Up", use_container_width=True, type="primary"):
            if not username or not email or not password:
                st.error("Please fill in all fields")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            if len(password) < 6:
                st.error("Password must be at least 6 characters")
                return
            
            try:
                with st.spinner("Creating account..."):
                    result = api_client.signup(username, email, password)
                    token = result.get("access_token")
                    
                    if token:
                        api_client.set_token(token)
                        user_info = api_client.get_current_user()
                        set_logged_in(token, user_info)
                        st.success("✅ Account created and logged in!")
                        st.rerun()
                    else:
                        st.error("❌ Signup failed")
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 409:
                    st.error("❌ Email already exists")
                else:
                    st.error(f"❌ Signup error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
        
        st.markdown("---")
        st.markdown("Already have an account? Switch to **Login** →")
    
    with col2:
        st.markdown("### Why Sign Up?")
        st.markdown("""
        ✅ **Benefits:**
        
        - 📖 Access to multiple documents
        - 💾 Save chat history
        - 🔄 Continue conversations
        - ⚡ Faster responses
        - 🎯 Personalized experience
        
        **Completely Free!**
        """)


def auth_screen(api_client: APIClient):
    """Main authentication screen with login/signup tabs"""
    
    # Header
    st.markdown("""
    <h1 style="text-align: center; color: #FF6B35;">🤖 RAG Chatbot</h1>
    <p style="text-align: center; color: gray;">Intelligent Document Q&A with Citation Tracking</p>
    <hr>
    """, unsafe_allow_html=True)
    
    # Tabs for login/signup
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        login_screen(api_client)
    
    with tab2:
        signup_form(api_client)
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: gray; font-size: 0.8em;">
        Built with Streamlit + FastAPI | Secure & Private | 2024
    </div>
    """, unsafe_allow_html=True)
