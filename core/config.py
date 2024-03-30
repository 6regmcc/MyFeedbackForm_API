import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # Database
    DB_USER: str = os.environ.get("POSTGRESQL_USER")
    DB_PASSWORD: str = os.environ.get("POSTGRESQL_PASSWORD")
    DB_NAME: str = os.environ.get("POSTGRESQL_DB")
    DB_HOST: str = os.environ.get("POSTGRESQL_SERVER")
    DB_PORT: str = os.environ.get("POSTGRESQL_PORT")
    DATABASE_URL: str = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    POSTGRESQL_URL: str = os.environ.get("POSTGRESQL_URL")

    # JWT
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "77dbf997d69675b8e6bf182804330523cf4dfc9842ea0c899d2cc9504c5dadf5")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("JWT_TOKEN_EXPIRE_MINUTES", 60)


def get_setting() -> Settings:
    return Settings()
