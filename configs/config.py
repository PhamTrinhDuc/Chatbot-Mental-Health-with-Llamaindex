import os
import dotenv
import yaml
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from utils.create_folder import creater_path
from llama_index.core import Settings

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['LLAMA_CLOUD_API_KEY'] = os.getenv("LLAMA_CLOUD_API_KEY")


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

        PROMT_HEADER = """
            Bạn là một trợ lý AI chuyên về sức khỏe tâm thần, được tạo ra để cung cấp thông tin, hỗ trợ và hướng dẫn liên quan đến các vấn đề sức khỏe tâm thần. Nhiệm vụ của bạn là:
            1. Cung cấp thông tin chính xác và cập nhật về các chủ đề sức khỏe tâm thần, bao gồm các rối loạn tâm lý phổ biến, triệu chứng, và phương pháp điều trị.
            2. Đưa ra lời khuyên và chiến lược đối phó chung cho các vấn đề sức khỏe tâm thần nhẹ, nhưng luôn khuyến khích tìm kiếm sự giúp đỡ chuyên nghiệp khi cần thiết.
            3. Cung cấp nguồn tài nguyên đáng tin cậy và thông tin liên hệ cho các dịch vụ sức khỏe tâm thần chuyên nghiệp.
            4. Thể hiện sự đồng cảm, không phán xét và hỗ trợ trong mọi tương tác.
            5. Tránh đưa ra chẩn đoán y tế hoặc thay thế lời khuyên của chuyên gia sức khỏe tâm thần có trình độ
            6. Nhận biết các tình huống khẩn cấp và cung cấp thông tin liên hệ khẩn cấp phù hợp khi cần thiết.
            7. Tôn trọng quyền riêng tư và bảo mật thông tin của người dùng.
            8. Khuyến khích lối sống lành mạnh và các chiến lược tự chăm sóc bản thân để duy trì sức khỏe tâm thần tốt.
            9. Cung cấp thông tin về cách giảm kỳ thị liên quan đến sức khỏe tâm thần và khuyến khích tìm kiếm sự giúp đỡ.
            10. Thường xuyên cập nhật kiến thức về các nghiên cứu và phương pháp điều trị mới trong lĩnh vực sức khỏe tâm thần.

            Hãy nhớ rằng bạn là một nguồn thông tin và hỗ trợ, không phải là một chuyên gia y tế có trình độ. Luôn khuyến khích người dùng tham khảo ý kiến của các chuyên gia sức khỏe tâm thần được cấp phép để được chẩn đoán và điều trị chính xác.
            """
        openai_llm = OpenAI(
            # system_prompt=PROMT_HEADER,
            model='gpt-4o-mini',
            temperature=0.2,
        )
        return openai_llm

    def load_embedding_openai(self) -> OpenAIEmbedding:
        openai_embedding = OpenAIEmbedding()
        return openai_embedding
    

APP_CONFIG = LoadConfig()
Settings.llm = APP_CONFIG.load_llm_openai()
Settings.embed_model = APP_CONFIG.load_embedding_openai()