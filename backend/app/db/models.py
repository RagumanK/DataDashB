from sqlalchemy import Column, Integer, String, Date, Time, Sequence
from app.db.base import Base

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, Sequence("fakemodel_id_sequence"), primary_key=True)
    product = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(Date, nullable=False)
    order_time = Column(Time, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
