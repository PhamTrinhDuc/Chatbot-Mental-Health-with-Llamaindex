import os
import logging
import json
import streamlit as st
from llama_index.core.storage.chat_store import SimpleChatStore
from configs.config import Config

CONVERSATION_FILE = Config.conversation_file
USER_AVT = Config.logo_user_path
PROFESSOR_AVT = Config.logo_bot_path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_chat_history() -> SimpleChatStore:
    """
    Hàm để khởi tạo hoặc load lại lịch sử cuộc trò chuyện
    """
    if os.path.join(CONVERSATION_FILE) and os.path.getsize(CONVERSATION_FILE) > 0:
        try:
            chat_history = SimpleChatStore.from_persist_path(CONVERSATION_FILE)
        except json.JSONDecodeError:
            chat_history = SimpleChatStore()
    else:
        chat_history = SimpleChatStore()
    return chat_history

def display_message(chat_store: SimpleChatStore, container, key: str) -> None:
    """
    Hàm để hiển thị tin nhắn trong cuộc trò chuyện giữa người dùng và chatbot
    Args:
        - chat_store: Lưu trữ cuộc trò chuyện
        - container: Container để hiển thị cuộc trò chuyện
        - key: Tên người dùng
    """
    with container:
        for message in chat_store.get_messages(key=key):
            if message.role == "user":
                with st.chat_message(message.role, avatar=USER_AVT):
                    st.markdown(message.content)
            if message.role == "assistant" and message.content != None:
                with st.chat_message(message.role, avatar=PROFESSOR_AVT):
                    st.markdown(message.content)
