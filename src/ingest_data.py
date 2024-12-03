from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import SummaryExtractor
from llama_index.embeddings.openai import OpenAIEmbedding
from configs.config import Config
from src.prompt import CUSTORM_SUMMARY_EXTRACT_TEMPLATE
from common.utils import logger


def ingest_documents(data_path: str = None):
    if data_path is None:
        data_path = Config.data_path
    if isinstance(data_path, str):
        data_path = [data_path]

    documents = SimpleDirectoryReader(
        input_files=data_path, 
        filename_as_id = True
    ).load_data()
    for doc in documents:
        print(doc.id_)
    
    try: 
        cached_hashes = IngestionCache.from_persist_path(
            Config.cache_data_path
            )
        logger.warning("Cache file found. Running using cache...")
    except:
        cached_hashes = ""
        logger.warning("No cache file found. Running without cache...")
    pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(
                chunk_size=512, 
                chunk_overlap=20
            ),
            SummaryExtractor(summaries=['self'], 
                             prompt_template=CUSTORM_SUMMARY_EXTRACT_TEMPLATE),
            OpenAIEmbedding()
        ],
        cache=cached_hashes
    )
   
    nodes = pipeline.run(documents=documents)
    pipeline.cache.persist(Config.cache_data_path)
    return nodes


def indexing_data():
    nodes = ingest_documents(data_path=Config.data_path)
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=Config.index_storage_path
        )
        vector_index = load_index_from_storage(
            storage_context, index_id="vector"
        )
        logger.info("All indices loaded from storage.")
    except Exception as e:
        logger.warning(f"Error occurred while loading indices: {e}")
        storage_context = StorageContext.from_defaults()
        vector_index = VectorStoreIndex(
            nodes, storage_context=storage_context
        )
        vector_index.set_index_id("vector")
        storage_context.persist(
            persist_dir=Config.index_storage_path
        )
        logger.info("New indexes created and persisted.")
    return vector_index
    