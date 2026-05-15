import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
print(f"DEBUG: La URL cargada es: {os.getenv('DB_URL')}")

DATABASE_URL = os.getenv("DB_URL", "mysql+pymysql://user:password@localhost:3306/db_name")

engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,  
    pool_recycle=3600    
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()