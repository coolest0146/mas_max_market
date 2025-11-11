# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
# Update with your MySQL credentials
# DATABASE_URL =os.getenv("DATABASE_URL")



engine = create_engine("mysql+pymysql://root:root@localhost:3306/MasmaxNexus")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()