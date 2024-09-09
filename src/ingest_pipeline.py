import os
from typing import List
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter, TokenTextSplitter
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.schema import TextNode
from configs.configurator import APP_CONFIG
from src.prompt import CUSTORM_SUMMARY_EXTRACT_TEMPLATE
from log import set_logging_error, set_logging_terminal

LOG_ERROR = set_logging_error()
LOG_TERMINAL = set_logging_terminal()
EMBEDDING_MODEL = APP_CONFIG.load_embedding_openai()
CACHE_FILE = APP_CONFIG.cache_file


def ingest_documents() -> List[TextNode]:

    input_files = [os.path.join(APP_CONFIG.data_path, file_name) 
                   for file_name in os.listdir(APP_CONFIG.data_path)]
    documents = SimpleDirectoryReader(
        input_files=input_files,
        filename_as_id=True
    ).load_data()

    text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=128)
    nodes = text_splitter(documents) 

    return nodes

    try:
        cached_hashes = IngestionCache.from_persist_path(
            CACHE_FILE
        )
        LOG_TERMINAL.info("INGEST_PIPELINE.PY: Cache file found. Running using cache...")
    except:
        cached_hashes = ""
        LOG_ERROR.info("INGEST_PIPELINE.PY: Cache file not found. Running without cache...")
    
    transformations = [
        TokenTextSplitter(chunk_size=512, chunk_overlap=128),
        TitleExtractor(nodes=5),
        QuestionsAnsweredExtractor(questions=3),
        EMBEDDING_MODEL
    ]
    
    pipeline = IngestionPipeline(
        transformations=transformations,
        cache=cached_hashes
    )

    nodes = pipeline.run(documents = documents)
    # print(type(nodes[0]))
    pipeline.cache.persist(CACHE_FILE)

    return nodes