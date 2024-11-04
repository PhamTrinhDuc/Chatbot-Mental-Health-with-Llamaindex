import os
import json
import streamlit as st
from datetime import datetime
from llama_index.core import load_index_from_storage, get_response_synthesizer, VectorStoreIndex
from llama_index.core.storage import StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.retrievers import VectorIndexRetriever
# from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import FunctionTool
from configs.config import APP_CONFIG
from src.prompt import CUSTORM_AGENT_SYSTEM_TEMPLATE


USER_AVT = APP_CONFIG.logo_user
PROFESSOR_AVT = APP_CONFIG.logo_bot
CONVERSATION_FILE = APP_CONFIG.conversation_file

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
        "Content": content,
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
            

def create_retriever() -> RetrieverQueryEngine:
    # chroma_client = chromadb.EphemeralClient()
    # chroma_collection = chroma_client.create_collection("quickstart")

    # vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(persist_dir=APP_CONFIG.index_storage)
                                                #    vector_store=vector_store)

    index = load_index_from_storage(storage_context=storage_context, vector_id="vector")
    
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=3,
    )
    # response_synthetizer = get_response_synthesizer(
    #     response_mode="tree_summarize",
    #     verbose=False
    # )
    # post_process = SimilarityPostprocessor(similarity_cutoff=0.5)
    dsm5_engine = RetrieverQueryEngine(
        retriever=retriever,
        # response_synthesizer=response_synthetizer,
        # node_postprocessors=[post_process]

    )
    return dsm5_engine


def initlize_chatbot(chat_store: SimpleChatStore, container, username: str, user_info: str) -> OpenAIAgent:
    
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
    
    dsm5_engine = create_retriever()
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
        tools=[dsm5_tool, save_tool],
        memory=memory,
        system_prompt=CUSTORM_AGENT_SYSTEM_TEMPLATE.format(user_info=user_info),
        verbose=True
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
                st.markdown("Chào bạn, mình là Chatbot MENTHAL HEALTH được phát triển bởi PTIT. Mình sẽ giúp bạn chăm sóc sức khỏe tinh thần. Hãy cho mình biết tình trạng của bạn hoặc bạn có thể trò chuyện với mình nhé!")
    if st.session_state.logged_in:
        username = st.session_state.username
        user_info = st.session_state.user_info
        st.subheader("💬 LLAMA-INDEX MENTAL HEALTH")
        container = st.container()
        chat_history = load_chat_history()
        chatbot = initlize_chatbot(chat_store=chat_history, 
                                   container=st.container(), 
                                   username=username, 
                                   user_info=user_info)
        chat_interface(agent=chatbot, 
                       chat_store=chat_history, 
                       container=container)
    user_input = st.text_input("Nhập tin nhắn của bạn tại đây...",)
    if user_input:
        with container:
            with st.chat_message(name="user", avatar=USER_AVT):
                st.markdown(user_input)
            response = str(agent.chat(user_input))
            with st.chat_message(name="assistant", avatar=PROFESSOR_AVT):
                st.markdown(response)
        chat_store.persist(CONVERSATION_FILE)