from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# Import the DuckDB dialect explicitly
import duckdb_engine
engine = create_engine(settings.DATABASE_URL)
print(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()
