import os
from dotenv import load_dotenv

load_dotenv()  # Carga el archivo .env que está al lado de main.py

class Settings:
    DATABASE_URL: str = os.getenv("DB_URL", "mysql+pymysql://user:password@localhost:3306/db_name")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")

settings = Settings()