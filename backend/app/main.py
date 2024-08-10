from fastapi import FastAPI
from app.api.v1.endpoints import orders
from app.db.init_db import init_db

app = FastAPI()

# Include the orders router
app.include_router(orders.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
