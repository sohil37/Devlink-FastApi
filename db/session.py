from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core import config

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()