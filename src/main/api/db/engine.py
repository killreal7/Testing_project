from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.api.config.config import Config

engine = create_engine(Config.fetch('DataBaseUrl'), echo=False)
SessionLocal = sessionmaker(bind=engine)