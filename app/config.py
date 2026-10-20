from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "OmniDoc AI"
    app_env: str = "development"
    max_upload_mb: int = 15
    chunk_size: int = 900
    chunk_overlap: int = 120
    retrieval_top_k: int = 4
    vector_store_dir: str = "data/chroma"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
