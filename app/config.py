from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


print("ENV PATH:", BASE_DIR / ".env")
print("EXISTS:", (BASE_DIR / ".env").exists())

from dotenv import dotenv_values
print(dotenv_values(BASE_DIR / ".env"))


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
