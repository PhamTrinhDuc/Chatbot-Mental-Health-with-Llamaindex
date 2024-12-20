import os
import json 
from datetime import datetime
from llama_index.core import StorageContext, load_index_from_storage
from common import logger
from configs.config import Config


def build_query_engine():
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=Config.index_storage_path
        )
        index = load_index_from_storage(
            storage_context, index_id="vector"
        )
        dsm5_engine = index.as_query_engine(
            llm=None,
            similarity_top_k=3,
        )
        return dsm5_engine
    
    except Exception as e:
        logger.error("Error occurred while build query engine: " + str(e))



def save_score(score: str, content: str, total_guess: str, username:str) -> None:
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
