from src import ingest_documents
from src import build_indexes

def main():

    # load data and run pipeline to get nodes =====================================
    nodes = ingest_documents()
    # print(nodes[0].text)

    # indexing nodes into the database ============================================
    vector_index = build_indexes(nodes)
    # query_engine = vector_index.as_query_engine()
    # response = query_engine.query("Rối loạn phát triển trí tuệ là gì ?")
    # print(response)

if __name__ == "__main__":
    main()