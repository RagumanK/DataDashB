from fastapi import APIRouter, HTTPException
from app.schemas.order import Order
from app.services.order_service import OrderService

router = APIRouter()

@router.post("/orders/")
def create_order(order: Order):
    return OrderService.create_order(order)

@router.get("/orders/{order_id}")
def read_order(order_id: int):
    order = OrderService.read_order(order_id)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")

@router.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    updated_order = OrderService.update_order(order_id, order)
    if updated_order:
        return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/orders/{order_id}")
def delete_order(order_id: int):
    deleted = OrderService.delete_order(order_id)
    if deleted:
        return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")

@router.get("/orders/")
def list_orders():
    return OrderService.list_orders()
