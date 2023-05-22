from pydantic import BaseSettings
import os

class SettingsManager(BaseSettings):
    BASE_URL: str = "http://localhost:8000"
    USE_NGROK: bool = os.environ.get("USE_NGROK", "False") == "True"

    class Config:
        env_file = ".env"
