from app.db.base import Base
from app.db.session import engine
from app.utils.csv_loader import load_data_from_csv
from sqlalchemy import inspect


def init_db():
    # Create all tables
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Check if the table exists
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if 'orders' not in tables:
        print("Table 'orders' was not created.")
        return
    
    # Load data from CSV after confirming table creation
    load_data_from_csv('data/orders.csv', engine)