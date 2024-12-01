import chromadb
from llama_index.core import SimpleDirectoryReader
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding


def ingest_data(data_dir: str = "./data/dsm-5-cac-tieu-chuan-chan-doan.docx"):
    documents = SimpleDirectoryReader(
        input_files=[data_dir],
    ).load_data()
    
    embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    
    chroma_client = chromadb.PersistentClient(path="./data/vector_db")
    chroma_collection = chroma_client.get_or_create_collection("test")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, 
        embed_model=embed_model, show_progress=True
    )
    
if __name__ == "__main__":
    ingest_data()