from typing import List
from llama_index.core.schema import TextNode
from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core import StorageContext
from configs.configurator import APP_CONFIG
from log import LOG_TERMINAL, LOG_ERROR

def build_indexes(nodes: List[TextNode]) -> VectorStoreIndex:
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=APP_CONFIG.index_storage
        )
        vector_index = load_index_from_storage(
            storage_context, index_id="vector"
        )
        LOG_TERMINAL.info("INDEX_BUILDER.PY: All indices loaded from storage")

    except Exception as e:
        LOG_ERROR.info(f"INDEX_BUILDER.PY: Error occurred while loading indices: {e}")
        storage_context = StorageContext.from_defaults()
        vector_index = VectorStoreIndex(
            nodes, storage_context=storage_context
        )
        vector_index.set_index_id("vector")
        storage_context.persist(
            persist_dir=APP_CONFIG.index_storage
        )
        LOG_TERMINAL.info("INDEX_BUILDER.PY: New indexes created and persisted")
    return vector_index