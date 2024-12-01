import chromadb
import os
import json 
from datetime import datetime
from typing import List
from llama_index.core.schema import TextNode
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from src.models import using_embedding_openai
from common import logger
from configs.config import Config

def build_query_engine() -> VectorStoreIndex:
    try:
        embed_model = using_embedding_openai(api_key=os.getenv("OPENAI_API_KEY"))
        chroma_client = chromadb.PersistentClient(path="./data/vector_db")
        chroma_collection = chroma_client.get_or_create_collection("test")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        KB_index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context, embed_model=embed_model, show_progress=True
        )
        query_engine = KB_index.as_query_engine(
            llm = None,
            similarity_top_k = 2,
            vector_store_query_node = "hybrid"
        )

        return query_engine
    except Exception as e:
        logger.error("Error occurred while build query engine")


import json
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

def save_score(score, content, total_guess, username):
    """
    Hàm để lưu kết quả chẩn đoán của người dùng
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {
        "username": username,
        "Time": current_time,
        "Score": score,
        "Content": content,
        "Total guess": total_guess,
    }

    # Kiểm tra và đọc file JSON
    data = []
    if os.path.exists(Config.scores_file_path):
        try:
            with open(Config.scores_file_path, "r") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from file: {e}")
        except IOError as e:
            logger.error(f"Error reading score file: {e}")

    # Thêm dữ liệu mới
    data.append(new_entry)

    # Ghi file JSON
    try:
        with open(Config.scores_file_path, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        logger.error(f"Error writing to score file: {e}")
