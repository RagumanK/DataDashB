import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = "duckdb:///./data/orders.db"

settings = Settings()
