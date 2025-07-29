import streamlit as st
from utils.full_chain import get_response

def main():
    st.set_page_config(page_title="RAG Customer Support", page_icon="🤖", layout="centered")
    st.title("`RAG Customer Support`")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    user_query = st.chat_input("Ask a question:")
    if user_query:
        response = get_response(user_query=user_query, chat_history=st.session_state.chat_history)
        st.session_state.chat_history.append((user_query, response['answer'].strip()))
        
        for chat, answer in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat)
            with st.chat_message("assistant"):
                st.write(answer)
        
        with st.expander(label="Source Documents"):
            source_documents = [doc.page_content for doc in response['source_documents']]
            # st.write(source_documents)
            st.write(response['source_documents'])


if __name__ == "__main__":
    main()