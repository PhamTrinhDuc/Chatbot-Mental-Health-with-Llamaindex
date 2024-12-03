import os
from typing import Literal
from src.prompt import PROMT_HEADER
from llama_index.llms.openai import OpenAI
from llama_index.llms.groq import Groq 
from llama_index.embeddings.openai import OpenAIEmbedding
from common import logger


def using_llm_openai(
        api_key: str = None, 
        model_name: Literal["gpt-4o-mini", 
                            "gpt-3.5-turbo", 
                            "gpt-4o", 
                            "gpt-4-turbo"] = "gpt-4o-mini") -> OpenAI:
    try:
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            openai_llm = OpenAI(
                system_prompt=PROMT_HEADER,
                model=model_name,
                temperature=0.2,
            )
            return openai_llm
        else:
            logger.warning("Plese enter api key OpenAI")
    except Exception as e:
        logger.error(f"Error occurred: {e}")

def using_llm_groq(
    api_key: str = None,
    model_name: Literal["llama3-70b-8192", 
                   "llama-3.1-70b-versatile", 
                   "llava-v1.5-7b-4096-preview", 
                   "gemma2-9b-it", 
                   "mixtral-8x7b-32768",] = "llama-3.1-70b-versatile",) -> Groq:
    try:
        if api_key:
            os.environ['GROQ_API_KEY'] = api_key
            groq_llm = Groq(model=model_name)
            return groq_llm
        else:
            logger.warning("Plese enter api key Groq")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        

def using_embedding_openai(api_key: str,
                          model_name: str = "text-embedding-3-large") -> OpenAIEmbedding:
    try:
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            openai_embedding = OpenAIEmbedding(model=model_name)
            return openai_embedding
        else:
            logger.warning("Plese enter api key OpenAI")
    except Exception as e:
        logger.error(f"Error occurred: {e}")