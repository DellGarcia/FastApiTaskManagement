from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.configs.settings import settings


class Config:

    @staticmethod
    def get_database_url():
        if settings.DATABASE_TYPE == 'sqlite':
            return f'sqlite:///{Path(__file__).parent.parent}/database.db'
        raise ValueError("Invalid database type.")


engine = create_engine(Config.get_database_url(), echo=False,
                       connect_args={'check_same_thread': False} if settings.DATABASE_TYPE == 'sqlite' else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
