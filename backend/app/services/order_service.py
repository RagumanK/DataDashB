from sqlalchemy.orm import Session
from app.db.models import Order
from app.schemas.order import Order
from app.db.session import session

class OrderService:
    @staticmethod
    def create_order(order: Order):
        new_order = Order(**order.dict())
        session.add(new_order)
        session.commit()
        return new_order

    @staticmethod
    def read_order(order_id: int):
        return session.query(Order).filter(Order.order_id == order_id).first()

    @staticmethod
    def update_order(order_id: int, order: Order):
        existing_order = session.query(Order).filter(Order.order_id == order_id).first()
        if not existing_order:
            return None
        for key, value in order.dict().items():
            setattr(existing_order, key, value)
        session.commit()
        return existing_order

    @staticmethod
    def delete_order(order_id: int):
        existing_order = session.query(Order).filter(Order.order_id == order_id).first()
        if not existing_order:
            return None
        session.delete(existing_order)
        session.commit()
        return True

    @staticmethod
    def list_orders():
        return session.query(Order).all()
