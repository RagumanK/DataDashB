from sqlalchemy.orm import Session
from app.db.models import Order as OrderModel  # SQLAlchemy model
from app.schemas.order import Order as OrderSchema  # Pydantic schema
from app.db.session import session

class OrderService:
    @staticmethod
    def create_order(order: OrderSchema):
        new_order = OrderModel(**order.dict())
        session.add(new_order)
        session.commit()
        return new_order

    @staticmethod
    def read_order(order_id: int):
        return session.query(OrderModel).filter(OrderModel.order_id == order_id).first()

    @staticmethod
    def update_order(order_id: int, order: OrderSchema):
        existing_order = session.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        if not existing_order:
            return None
        for key, value in order.dict().items():
            setattr(existing_order, key, value)
        session.commit()
        return existing_order

    @staticmethod
    def delete_order(order_id: int):
        existing_order = session.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        if not existing_order:
            return None
        session.delete(existing_order)
        session.commit()
        return True

    @staticmethod
    def list_orders():
        return session.query(OrderModel).limit(50).all()