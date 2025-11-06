from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import Config
from src.database.models import Base

engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
