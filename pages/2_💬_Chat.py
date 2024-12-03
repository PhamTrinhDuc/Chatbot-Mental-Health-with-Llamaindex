import streamlit as st
from typing import List, Dict
from src import initlize_chatbot, chat_interface
from common.utils import load_chat_history
from ui.sidebar import show_sidebar 

def main():
    show_sidebar()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        username = st.session_state.username
        user_info = st.session_state.user_info
        st.subheader("💬 Trò chuyện với chuyên gia tâm lý AI")
        chat_history = load_chat_history()
        container = st.container()
        chatbot = initlize_chatbot(chat_store=chat_history, 
                                   container=container, 
                                   username=username, 
                                   user_info=user_info)
        
        chat_interface(agent=chatbot, 
                       chat_store=chat_history, 
                       container=container)

if __name__ == "__main__":
    main()