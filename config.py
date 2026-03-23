from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = os.getenv('APP_NAME', 'todo-app')
    APP_DESCRIPTION: str = os.getenv('APP_DESCRIPTION', 'A REST API for managing todo items')
    SUPABASE_URL: str = os.getenv('SUPABASE_URL')
    SUPABASE_KEY: str = os.getenv('SUPABASE_KEY')
    JWT_SECRET: str = os.getenv('JWT_SECRET')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 60))

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()

def get_settings() -> Settings:
    return settings