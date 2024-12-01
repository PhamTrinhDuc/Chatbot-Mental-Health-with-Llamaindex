import os
import streamlit as st
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import FunctionTool
from src.models import using_llm_openai
from src.prompt import CUSTORM_AGENT_SYSTEM_TEMPLATE
from src.tools import build_query_engine, save_score
from common import display_message, load_chat_history
from configs.config import Config

CONVERSATION_FILE = Config.conversation_file
USER_AVT = Config.logo_user_path
PROFESSOR_AVT = Config.logo_bot_path



def initlize_chatbot(chat_store: SimpleChatStore, container, username: str, user_info: dict) -> OpenAIAgent:
    
    """
    Xây dựng tool truy vấn từ cơ sở dữ liệu và tool lưu trữ kết quả chẩn đoán từ đó tạo agent để trò chuyện với người dùng.
    Args:
        - chat_store: Lưu trữ cuộc trò chuyện
        - container: Container để hiển thị cuộc trò chuyện
        - username: Tên người dùng
        - user_infor: Thông tin người dùng
    Return:
        - agent: Agent để trò chuyện với người dùng
    """
    
    memory = ChatMemoryBuffer(
        chat_store=chat_store, 
        token_limit=3000,
        chat_store_key=username)
    
    dsm5_engine = build_query_engine()
    dsm5_tool=QueryEngineTool(
        query_engine=dsm5_engine,
        metadata=ToolMetadata(
            name="DSM-5",
            description=(
                f" Cung cấp các thông tin liên quan đến các bệnh "
                f"tâm thần theo tiêu chuẩn DSM5 . Sử dụng câu hỏi văn bản thuần túy chi tiết làm đầu vào cho công cụ"
            ),
        )
    )

    save_tool = FunctionTool.from_defaults(fn=save_score)
    agent = OpenAIAgent.from_tools(
        llm=using_llm_openai(api_key=os.getenv("OPENAI_API_KEY")),
        tools=[dsm5_tool, save_tool],
        memory=memory,
        system_prompt=CUSTORM_AGENT_SYSTEM_TEMPLATE.format(user_info=user_info),
    )
    display_message(chat_store, container, key=username)
    return agent


def chat_interface(agent: OpenAIAgent, chat_store: SimpleChatStore, container) -> None:
    """
    hàm để hiển thị giao diện trò chuyện giữa người dùng và chatbot
    Args:
        - agent: Agent để trò chuyện với người dùng
        - chat_store: Lưu trữ cuộc trò chuyện
        - container: Container để hiển thị cuộc trò chuyện
    """
    if not os.path.exists(CONVERSATION_FILE) or os.path.getsize(CONVERSATION_FILE) == 0:
        with container:
            with st.chat_message(name="assistant", avatar=PROFESSOR_AVT):
                st.markdown("Chào bạn, mình là Chatbot MENTHAL HEALTH được phát triển bởi PTIT Nhóm 17. Mình sẽ giúp bạn chăm sóc sức khỏe tinh thần. Hãy cho mình biết tình trạng của bạn hoặc bạn có thể trò chuyện với mình nhé!")
    
    user_input = st.chat_input("Nhập tin nhắn của bạn tại đây...",)
    if user_input:
        with container:
            with st.chat_message(name="user", avatar=USER_AVT):
                st.markdown(user_input)
            response = str(agent.chat(user_input))
            with st.chat_message(name="assistant", avatar=PROFESSOR_AVT):
                st.markdown(response)
        chat_store.persist(CONVERSATION_FILE)