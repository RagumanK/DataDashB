from app.db.base import Base
from app.db.session import engine
from app.utils.csv_loader import load_data_from_csv
from sqlalchemy import inspect
from app.db.models import Order  # Adjust the path based on your project structure

def init_db():
    # Create all tables based on the Base metadata
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"An error occurred during table creation: {e}")
        return  # Exit the function if table creation fails

    # Inspect the database to check if the 'orders' table exists
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if 'orders' not in tables:
        print("Table 'orders' was not created.")
        return
    
    # Load data from a CSV file into the 'orders' table after confirming the table's existence
    try:
        load_data_from_csv('data/orders.csv', engine)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"An error occurred during data loading: {e}")
