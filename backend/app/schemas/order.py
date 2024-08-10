from pydantic import BaseModel

class Order(BaseModel):
    product: str
    quantity: int
    price: int
    order_date: str  # YYYY-MM-DD format
    order_time: str  # HH:MM:SS format
    address: str
    city: str
    product_type: str

    class Config:
        from_attributes = True
