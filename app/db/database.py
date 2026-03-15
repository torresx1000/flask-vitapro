from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import Config

Base = declarative_base()

engine = create_engine(
    Config.DATABASE_URI,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine)

# Global session (simple singleton for this app)
session = SessionLocal()


def init_db():
    Base.metadata.create_all(bind=engine)
