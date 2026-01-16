from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROXY_PORT: int = 5001
    LUNA_CACHE_PATH: str = "luna_cache.db"
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_API_KEY: str = "sk-..."
    
    HISTORY_LINES: int = 10
    SUMMARY_EVERY_N_LINES: int = 50
    CONTEXT_PLACEHOLDER: str = "{{CONTEXT}}"
    
    DATA_DIR: str = "data"
    STATE_FILE: str = "data/state.json"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
