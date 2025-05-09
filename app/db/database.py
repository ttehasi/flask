from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from app.db.models import Base


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)

session_factory = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)