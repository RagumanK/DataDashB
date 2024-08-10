import pandas as pd
from app.db.models import Order
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def load_data_from_csv(file_path: str, engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        order = Order(
            product=row['product'],
            quantity=row['quantity'],
            price=row['price'],
            order_date=row['order_date'],
            order_time=row['order_time'],
            address=row['address'],
            city=row['city'],
            product_type=row['product_type']
        )
        session.add(order)
    session.commit()
    session.close()
