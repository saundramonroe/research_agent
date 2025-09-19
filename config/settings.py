# config/settings.py - Updated for Anaconda AI Navigator API
import os
from dataclasses import dataclass

@dataclass
class LocalSettings:
    MODEL_API_URL: str = "http://127.0.0.1:8080"
    MODEL_NAME: str = "Meta-Llama-3-8B-Instruct_Q4_K_M.gguf"
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 1500
    MAX_CONTEXT_LENGTH: int = 4096
    TOP_P: float = 0.9
    TOP_K: int = 40
    REPEAT_PENALTY: float = 1.1
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    ENABLE_DUCKDUCKGO: bool = False
    ENABLE_ARXIV: bool = True
    ENABLE_WIKIPEDIA: bool = True
    MAX_SEARCH_RESULTS: int = 10
    MAX_SOURCES_PER_QUERY: int = 7
    SEARCH_TIMEOUT: int = 10
    REQUESTS_PER_MINUTE: int = 20
    DELAY_BETWEEN_REQUESTS: float = 1.0
    VECTOR_DB_PATH: str = "data/vector_store"
    CACHE_DIR: str = "data/research_cache"
    OUTPUT_DIR: str = "outputs/reports"
    GRADIO_SERVER_NAME: str = "127.0.0.1"
    GRADIO_SERVER_PORT: int = 7862
    GRADIO_SHARE: bool = False
    ANONYMIZE_QUERIES_IN_LOGS: bool = True
    ENABLE_TELEMETRY: bool = False
    DEFAULT_CITATION_STYLE: str = "apa"
    DEFAULT_MAX_SOURCES: int = 7
    DEFAULT_INCLUDE_ACADEMIC: bool = True

settings = LocalSettings()

def setup_directories():
    directories = ["data/vector_store", "data/research_cache", "outputs/reports", "logs", "models"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Created directories")

setup_directories()
