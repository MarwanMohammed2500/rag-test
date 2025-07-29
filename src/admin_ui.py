import os
import streamlit as st
from utils.Load_data import loading_data
from utils.Vector_db import add_documents_to_pinecone

def main():
    st.set_page_config(layout="wide", page_icon="🤖", page_title="Admin RAG UI")
    st.title("`Admin RAG UI`")
    
    
    st.sidebar.title("`Upload Files or URL`")
    uploaded_files = st.sidebar.file_uploader("`Choose files`", 
                                              accept_multiple_files=True, type=["pdf", "docx", "txt"])
    url = st.sidebar.text_input("`Enter a YouTube URL:`",
                                placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    if st.sidebar.button("`Upload and Process Files`"):
        if uploaded_files and url:
            file_paths = []
            for path in uploaded_files:
                temp_file_path = os.path.join(os.getcwd(), path.name)
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(path.read())
                file_paths.append(temp_file.name)
                
            with st.spinner("`Processing files...`", show_time=True):
                data = loading_data(file_paths=file_paths, url=url)
                st.write(f"Length of Documents: {len(data)}")
                _ = add_documents_to_pinecone(documents=data)
                _ = [os.remove(file_path) for file_path in file_paths]
            st.success("✅ Files uploaded and processed successfully. 📁")
            
        elif uploaded_files:
            file_paths = []
            for path in uploaded_files:
                temp_file_path = os.path.join(os.getcwd(), path.name)
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(path.read())
                file_paths.append(temp_file.name)
                
            with st.spinner("`Processing files...`", show_time=True):
                data = loading_data(file_paths=file_paths)
                st.write(f"Length of Documents: {len(data)}")
                _ = add_documents_to_pinecone(documents=data)
                _ = [os.remove(file_path) for file_path in file_paths]
            st.success("✅ Files uploaded and processed successfully. 📁")
            
        elif url:
            with st.spinner("`Processing URL...`", show_time=True):
                data = loading_data(url=url)
                st.write(f"Length of Documents: {len(data)}")
                _ = add_documents_to_pinecone(documents=data)
                
        else: 
            st.warning("⚠️ Please upload files or enter a YouTube URL.")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("Created by [Osama Abo-Bakr](https://osama-abo-bakr.vercel.app/) with ❤️")
    
if __name__ == "__main__":
    main()