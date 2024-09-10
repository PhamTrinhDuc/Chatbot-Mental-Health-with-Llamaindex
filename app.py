from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from configs.configurator import APP_CONFIG
import chromadb
from llama_index.core.storage import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import Settings

documents = SimpleDirectoryReader(
    "data/ingestion_data",
    filename_as_id=True
).load_data()

text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=128)
nodes = text_splitter(documents) 


chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex(nodes, 
                            storage_context=storage_context, 
                            embed_model=APP_CONFIG.load_embedding_openai())
query_engine  = index.as_query_engine(similarity_top_k=3,
                                    vector_store_query_node="hybrid")


response = query_engine.query("giao tiếp ngôn ngữ")
print(response)