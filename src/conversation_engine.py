import os
import json
from datetime import datetime
import streamlit as st
from llama_index.core import load_index_from_storage, get_response_synthesizer
from llama_index.core.storage import StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import FunctionTool
from configs.configurator import APP_CONFIG
from src import CUSTORM_AGENT_SYSTEM_TEMPLATE


USER_AVT = APP_CONFIG.logo_user
PROFESSOR_AVT = APP_CONFIG.logo_bot
CONVERSATION_FILE = APP_CONFIG.conversation_file

def load_chat_history() -> SimpleChatStore:
    """
    Hàm để khởi tạo hoặc load lại lịch sử cuộc trò chuyện
    """
    if os.path.join(CONVERSATION_FILE) and os.paht.getsize(CONVERSATION_FILE) > 0:
        try:
            chat_history = SimpleChatStore.from_persist_path(CONVERSATION_FILE)
        except json.JSONDecodeError: 
            chat_history = SimpleChatStore()
    else:
        chat_history = SimpleChatStore()
    return chat_history


def save_score(score: str, content: str, total_guess: str, username: str) -> None:
    """
    Hàm để lưu kết quả chẩn đoán của người dùng
    Args: 
        - score: Điểm số của người dùng
        - content: Nội dung cuộc trò chuyện
        - total_guess: Tổng số lần đoán
        - username: Tên người dùng
    """
    curent_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {
        "username": username,
        "Time": curent_time,
        "Score": score,
        "Contetn": content,
        "Total Guess": total_guess
    }

    try:
        with open(APP_CONFIG.scores_file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(new_entry) #  thêm dữ liệu vào file
    with open(APP_CONFIG.scores_file_path, "w") as f: # ghi lại vào file
        json.dump(data, f, indent=4)


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
            

def initlize_chatbot(chat_store: SimpleChatStore, container, username: str, user_infor) -> OpenAIAgent:
    
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
        chat_store, 
        token_limit=3000,
        chat_store_key=username)
    
    storage_context = StorageContext.from_defaults(
        APP_CONFIG.index_storage
    )
    index = load_index_from_storage(storage_context, vector_id="vector")
    # dsm5_engine = index.as_query_engine(similarity_top_k=3)


    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=3
    )
    response_synthetizer = get_response_synthesizer(
        response_mode="tree_summarize",
        verbose=False
    )
    post_process = SimilarityPostprocessor(similarity_cutoff=0.5)
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthetizer=response_synthetizer,
        node_postprocessors=[post_process]
    )
    dsm5_tool=QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="DSM-5",
            description=(
                f" Cung cấp các thông tin liên quan đến các bệnh ",
                f"tâm thần theo tiêu chuẩn DSM5 . Sử dụng câu hỏi văn bản thuần túy chi tiết làm đầu vào cho công cụ"
            ),
        )
    )

    save_tool = FunctionTool.from_defaults(fn=save_score)
    agent = OpenAIAgent(
        tool=[dsm5_tool, save_tool],
        memory=memory,
        system_name=CUSTORM_AGENT_SYSTEM_TEMPLATE.format(user_infor=user_infor),
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
    if not os.path.join(os.path.exists(CONVERSATION_FILE) or os.path.getsize(CONVERSATION_FILE) == 0):
        with container:
            with st.chat_message(name="assistant", avatar=PROFESSOR_AVT):
                st.markdown("Chào bạn, mình là Chatbot MENTHAL HEALTH được phát triển bởi DUC PTIT. Mình sẽ giúp bạn chăm sóc sức khỏe tinh thần. Hãy cho mình biết tình trạng của bạn hoặc bạn có thể trò chuyện với mình nhé!")
    
    user_input = st.text_input("Nhập tin nhắn của bạn tại đây...",)
    if user_input:
        with container:
            with st.chat_message(name="user", avatar=USER_AVT):
                st.markdown(user_input)
            response = str(agent(user_input))
            with st.chat_message(name="assistant", avatar=PROFESSOR_AVT):
                st.markdown(response)
        chat_store.persist(CONVERSATION_FILE)