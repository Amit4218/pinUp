from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str
    RESOURCE_PAGE: str
    RESOURCE_ID: str
    RESOURCE_ORIGIN: str
    DOWNLOAD_DIR:Path = Path("temp")

    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings() # type: ignore