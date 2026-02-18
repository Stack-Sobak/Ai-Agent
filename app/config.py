from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    yandex_api_key: str
    yandex_cloud_folder: str
    assistant_id: str
    backend_url: str

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
