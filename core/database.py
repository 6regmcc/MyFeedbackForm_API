import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from core.config import get_setting
from sqlalchemy import MetaData


settings = get_setting()

engine = create_engine(
    #os.getenv("POSTGRESQL_URL"),
    os.environ.get("POSTGRESQL_URL"),
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    echo=True

)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
