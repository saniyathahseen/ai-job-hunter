import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Get the directory of this file (backend/app/core)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Travel up two folders to hit your main project root folder
# First split drops 'core', second split drops 'app'
APP_DIR = os.path.dirname(CURRENT_DIR)
BACKEND_DIR = os.path.dirname(APP_DIR)
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

class Settings(BaseSettings):
    DATABASE_URL: str
    
    # 3. Force Pydantic to read directly from the main project root
    model_config = SettingsConfigDict(
        env_file=os.path.join(PROJECT_ROOT, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
