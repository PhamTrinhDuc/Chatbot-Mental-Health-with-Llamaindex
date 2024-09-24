import os
from typing import List
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor, SummaryExtractor
from llama_index.core.schema import TextNode
from configs.configurator import APP_CONFIG
from src.prompt import (
    CUSTORM_SUMMARY_EXTRACT_TEMPLATE, 
    CUSTORM_TITLE_EXTRACT_TEMPLATE, 
    CUSTORM_QUESTION_GEN_TMPL,
    LLAMA_PARSE_PROMPT
)
from log import set_logging_error, set_logging_terminal

LOG_ERROR = set_logging_error()
LOG_TERMINAL = set_logging_terminal()
EMBEDDING_MODEL = APP_CONFIG.load_embedding_openai()
CACHE_FILE = APP_CONFIG.cache_file


def ingest_documents() -> List[TextNode]:

    input_files = [os.path.join(APP_CONFIG.data_path, file_name) 
                   for file_name in os.listdir(APP_CONFIG.data_path)]
    # using larma_parse to extract text from pdf files
    parser = LlamaParse(result_type="text",
                        parsing_instruction=LLAMA_PARSE_PROMPT)
    file_extractor = {".pdf": parser}

    documents = SimpleDirectoryReader(
        input_files=input_files,
        filename_as_id=True,
        file_extractor=file_extractor
    ).load_data()

    try:
        cached_hashes = IngestionCache.from_persist_path(
            CACHE_FILE
        )
        LOG_TERMINAL.info("INGEST_PIPELINE.PY: Cache file found. Running using cache...")
    except:
        cached_hashes = ""
        LOG_ERROR.info("INGEST_PIPELINE.PY: Cache file not found. Running without cache...")
    
    pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(
                chunk_size=512, 
                chunk_overlap=20
            ),
            SummaryExtractor(summaries=['self'], prompt_template=CUSTORM_SUMMARY_EXTRACT_TEMPLATE),
            TitleExtractor(nodes=5, node_template=CUSTORM_TITLE_EXTRACT_TEMPLATE),
            QuestionsAnsweredExtractor(questions=3, prompt_template=CUSTORM_QUESTION_GEN_TMPL),
            EMBEDDING_MODEL
        ],
        cache=cached_hashes
    )

    nodes = pipeline.run(documents = documents)
    # print(type(nodes[0]))
    pipeline.cache.persist(CACHE_FILE)

    return nodes