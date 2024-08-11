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

    def to_dict(self):
        """Convert the Order object to a dictionary."""
        return {
            "order_id": self.order_id,
            "product": self.product,
            "price": self.price,
            "quantity": self.quantity,
            "order_date": self.order_date.isoformat(),  # Convert to ISO format string
            "order_time": self.order_time.isoformat(),  # Convert to ISO format string
            "address": self.address,
            "city": self.city,
            "product_type": self.product_type
        }
