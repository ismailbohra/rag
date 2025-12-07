"""
Document Upload Component
Handles PDF file uploads with progress tracking
"""
import streamlit as st
from api_client import APIClient
import os


def document_upload(api_client: APIClient):
    """Document upload interface with file management"""
    
    st.markdown("### 📤 Upload Documents")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can upload multiple PDF files. They will be indexed for RAG search."
    )
    
    if uploaded_files:
        st.markdown(f"**Selected {len(uploaded_files)} file(s):**")
        
        # Display selected files
        for idx, file in enumerate(uploaded_files, 1):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.caption(f"{idx}. {file.name} ({file.size / 1024 / 1024:.2f} MB)")
            with col2:
                st.caption(f"PDF")
        
        st.markdown("---")
        
        # Upload button
        if st.button("⬆️ Upload Files", use_container_width=True, type="primary"):
            
            # Save files temporarily
            temp_dir = ".temp_uploads"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            file_paths = []
            
            # Save all files
            with st.spinner("Saving files..."):
                try:
                    for file in uploaded_files:
                        file_path = os.path.join(temp_dir, file.name)
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                        file_paths.append(file_path)
                except Exception as e:
                    st.error(f"Error saving files: {str(e)}")
                    st.stop()
            
            # Upload to backend
            if file_paths:
                with st.spinner("Uploading to server..."):
                    try:
                        response = api_client.upload_documents(file_paths)
                        
                        # Clean up temp files
                        for file_path in file_paths:
                            if os.path.exists(file_path):
                                os.remove(file_path)
                        
                        # Show results
                        st.success("✅ Files uploaded successfully!")
                        
                        if response.get("files_processed"):
                            st.markdown("**Processed files:**")
                            for file_info in response.get("files_processed", []):
                                st.caption(
                                    f"📄 {file_info.get('filename')} - "
                                    f"{file_info.get('chunks_created')} chunks created"
                                )
                        
                        st.balloons()
                        st.session_state.show_upload_success = True
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Upload failed: {str(e)}")
                        # Clean up on error
                        for file_path in file_paths:
                            if os.path.exists(file_path):
                                os.remove(file_path)
    
    else:
        st.info("👆 Select PDF files to upload them for RAG indexing")
    
    st.markdown("---")
    
    # Recent uploads info
    st.markdown("### 📚 Uploaded Documents")
    
    try:
        # Try to fetch uploaded files from backend
        st.caption("Documents are automatically indexed and ready for search")
        st.info(
            "📖 Upload PDF documents and ask questions about their content. "
            "The system will retrieve relevant sections and generate answers based on the documents."
        )
    except Exception as e:
        st.warning(f"Could not load document list: {str(e)}")
