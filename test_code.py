from src import ingest_documents
from src import build_indexes
from src import create_retriever
import re 

def main():

    # load data and run pipeline to get nodes =====================================
    nodes = ingest_documents()
    print(nodes[0].text)
    text = re.sub(r'\n', ' ', nodes[0].text.strip())
    print(text)
    print("=" * 100)

    # indexing nodes into the database ============================================
    # vector_index = build_indexes(nodes)
    # query_engine = vector_index.as_query_engine()
    # response = query_engine.query("liêt kê các loại rối loạn giao tiếp")
    # print(response)

    engine = create_retriever(nodes)
    response = engine.query("có mấy loại rối loạn giao tiếp ngôn ngữ")
    print(response)

    
    # initlize chatbot ============================================================
    # chat_history  = load_chat_history()
    # agent = initlize_chatbot(chat_store=chat_history, username="Duc", user_info="")
    # response = agent.query("các loại rối loạn giao tiếp là gì ?")
    # print(response)


if __name__ == "__main__":
    main()

    # llm = OpenAI()
    # print(llm.complete("Rối loạn phát triển trí tuệ là gì ?"))
