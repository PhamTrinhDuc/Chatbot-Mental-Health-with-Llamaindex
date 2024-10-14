from src import ingest_documents
from src import build_indexes
import re 

def main():

    # load data and run pipeline to get nodes =====================================
    nodes = ingest_documents()
    for node in nodes:
        node.text = re.sub(r'\n', ' ', node.text.strip())

    print(nodes[1].text)

    # indexing nodes into the database ============================================
    vector_index = build_indexes(nodes)
    query_engine = vector_index.as_query_engine()
    response = query_engine.query("rối loạn ngôn ngữ")
    print(response)

    # engine = create_retriever()
    # response = engine.query("có mấy loại rối loạn giao tiếp ngôn ngữ")
    # print(response)

    
    # initlize chatbot ============================================================
    # chat_history  = load_chat_history()
    # agent = initlize_chatbot(chat_store=chat_history, username="Duc", user_info="")
    # response = agent.query("các loại rối loạn giao tiếp là gì ?")
    # print(response)


if __name__ == "__main__":
    main()