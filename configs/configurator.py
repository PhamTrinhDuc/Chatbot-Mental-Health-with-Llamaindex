import os
import dotenv
import yaml
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from utils.create_folder import creater_path


dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class LoadConfig:
    def __init__(self):
        PATH_YAML = "./configs/config.yaml"
        with open(PATH_YAML, "r") as file:
            self.app_config = yaml.load(file, Loader=yaml.FullLoader)
        
        self.load_directories()

    
    def load_directories(self):
        self.cache_file = (
            self.app_config['directories']['cache']['cache_file']
        )
        creater_path(self.cache_file)

        self.conversation_file = (
            self.app_config['directories']['cache']['conversation_file']
        )
        creater_path(self.conversation_file)

        self.data_path = (
            self.app_config['directories']['ingestion']['data_path']
        )
        creater_path(self.data_path)

        self.index_storage = (
            self.app_config['directories']['index']['index_storage']
        )
        creater_path(self.index_storage)

        self.user_file_path = (
            self.app_config['directories']['user']['user_file_path']
        )
        creater_path(self.user_file_path)

        self.scores_file_path = (
            self.app_config['directories']['user']['scores_file_path']
        )
        creater_path(self.scores_file_path)

        self.logo_system = (
            self.app_config['directories']['images']['logo_system_path']
        )
        self.logo_user = (
            self.app_config['directories']['images']['logo_user_path']
        )
        self.logo_bot = (
            self.app_config['directories']['images']['logo_bot_path']
        )

    def load_llm_openai(self) -> OpenAI:
        openai_llm = OpenAI(
            # api_key=os.getenv('OPENAI_API_KEY'),
            model='gpt-4o-mini',
            temperature=0.2,
        )
        return openai_llm

    def load_embedding_openai(self) -> OpenAIEmbedding:
        openai_embedding = OpenAIEmbedding()
        return openai_embedding
    

    
APP_CONFIG = LoadConfig()