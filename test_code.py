from src.tools import build_query_engine
from src.ingest_data import ingest_data
from common.utils import load_chat_history
from src.conversation_engine import initlize_chatbot
from llama_index.core import Settings

Settings.llm = None


def main():
    # data_dir = "./data/dsm-5-cac-tieu-chuan-chan-doan.docx"
    # ingest_data(data_dir=data_dir)

    engine = build_query_engine()
    response = engine.query("rối loạn giao tiếp xã hội ")
    print("=" * 100)
    print(response.response)
    print("=" * 100)

    
    # initlize chatbot ============================================================
    chat_history  = load_chat_history()
    agent = initlize_chatbot(chat_store=chat_history, username="Duc", user_info="")
    response = agent.query("Cho tôi biết thông tin về Rối loạn giao tiếp xã hội")
    print(response)

if __name__ == "__main__":
    main()