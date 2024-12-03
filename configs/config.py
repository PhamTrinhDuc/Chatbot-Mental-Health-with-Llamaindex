import os
import dotenv
from dataclasses import dataclass
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
Settings.llm = OpenAI(model="gpt-4o-mini")


@dataclass
class Config:
    # data
    data_path: str = "data/dsm-5-cac-tieu-chuan-chan-doan.docx"
    cache_data_path: str = "data/cache/pipeline_cache.json"
    index_storage_path: str = "data/index_storage"
    # history
    conversation_file: str = "data/history/converstion.json"
    # storage vdb
    vdb_path: str = "data/vdb_storage"
    # user:
    user_file_path:str = 'data/user_storage/users.yaml'
    scores_file_path:str = 'data/user_storage/scores.json'
    # images:
    logo_system_path: str = 'images/Logo.png'
    logo_user_path: str = 'images/user.png'
    logo_bot_path: str = 'images/professor.png'