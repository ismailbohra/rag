"""
API Client for RAG Chatbot Backend
Handles authentication, sessions, and chat operations
"""
import requests
from typing import Dict, List, Optional
import json


class APIClient:
    """Client for communicating with FastAPI RAG backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.token = None
        self.session = requests.Session()
    
    def set_token(self, token: str):
        """Store JWT token for subsequent requests"""
        self.token = token
    
    def _headers(self) -> Dict[str, str]:
        """Get headers with authorization token"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    # ==================== AUTHENTICATION ====================
    
    def signup(self, username: str, email: str, password: str) -> Dict:
        """Register a new user"""
        url = f"{self.base_url}/auth/signup"
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def login(self, email: str, password: str) -> Dict:
        """Login user and get JWT token"""
        url = f"{self.base_url}/auth/login"
        payload = {"email": email, "password": password}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_current_user(self) -> Dict:
        """Get current authenticated user info"""
        url = f"{self.base_url}/auth/me"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    # ==================== CHAT SESSIONS ====================
    
    def get_sessions(self) -> List[Dict]:
        """Get all chat sessions for current user"""
        url = f"{self.base_url}/chats/sessions"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    def create_session(self, title: Optional[str] = None) -> Dict:
        """Create a new chat session"""
        url = f"{self.base_url}/chats/sessions"
        payload = {"title": title or "New Chat"}
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    def get_session_messages(self, session_id: str) -> List[Dict]:
        """Get all messages in a session"""
        url = f"{self.base_url}/chats/sessions/{session_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    def delete_session(self, session_id: str) -> Dict:
        """Delete a chat session"""
        url = f"{self.base_url}/chats/sessions/{session_id}"
        response = requests.delete(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    # ==================== CHAT / QUERY ====================
    
    def send_query(
        self, 
        query: str, 
        session_id: Optional[str] = None,
        top_k: int = 5
    ) -> Dict:
        """
        Send a query and get response with citations
        
        Args:
            query: User's question
            session_id: Optional session ID (creates new if None)
            top_k: Number of top documents to retrieve
        
        Returns:
            Response with answer and citations
        """
        url = f"{self.base_url}/query/"
        payload = {
            "query": query,
            "session_id": session_id,
            "top_k": top_k
        }
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    # ==================== FILE UPLOAD / INGESTION ====================
    
    def upload_documents(self, file_paths: List[str]) -> List[Dict]:
        """
        Upload PDF documents for ingestion
        
        Args:
            file_paths: List of local PDF file paths
        
        Returns:
            List of ingestion results (one per file)
        """
        url = f"{self.base_url}/ingest/upload"
        
        files = []
        for file_path in file_paths:
            with open(file_path, "rb") as f:
                files.append(("files", (file_path.split("/")[-1], f, "application/pdf")))
        
        # Use multipart form data for file upload
        response = requests.post(
            url, 
            files=files,
            headers={"Authorization": f"Bearer {self.token}"} if self.token else {}
        )
        response.raise_for_status()
        return response.json()
    
    def download_pdf(self, filename: str, save_path: str) -> bool:
        """
        Download a PDF reference document
        
        Args:
            filename: Name of file to download
            save_path: Local path to save file
        
        Returns:
            True if successful
        """
        url = f"{self.base_url}/ingest/files/{filename}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
