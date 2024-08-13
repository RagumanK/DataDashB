from fastapi import APIRouter, HTTPException
from app.schemas.order import Order
from app.services.order_service import OrderService
from app.core.sockets import sio_server  # Import sio here

router = APIRouter()

@router.post("/orders/")
async def create_order(order: Order):
    new_order = OrderService.create_order(order)
    await sio_server.emit('orderCreated', new_order.to_dict())  # Emit socket event
    return new_order

@router.get("/orders/{order_id}")
async def read_order(order_id: int):
    order = OrderService.read_order(order_id)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")

@router.put("/orders/{order_id}")
async def update_order(order_id: int, order: Order):
    updated_order = OrderService.update_order(order_id, order)
    print('Database Updated', update_order)
    if updated_order:
        await sio_server.emit('orderUpdated', updated_order.to_dict())  # Emit socket event
        return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    deleted = OrderService.delete_order(order_id)
    if deleted:
        await sio_server.emit('orderDeleted', {'order_id': order_id})  # Emit socket event
        return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")

@router.get("/orders/")
def list_orders():
    return OrderService.list_orders()
