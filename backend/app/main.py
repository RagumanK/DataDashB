from fastapi import FastAPI
from app.api.v1.endpoints import orders
from app.db.init_db import init_db
from app.core.sockets import sio  # Import sio from the new module
import socketio

app = FastAPI()

# Include the orders router
app.include_router(orders.router, prefix="/api/v1")

# Wrap the FastAPI app with Socket.IO middleware
app_sio = socketio.ASGIApp(sio, app)

@app.on_event("startup")
def on_startup():
    init_db()

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
async def disconnect(sid):
    print('Client disconnected:', sid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_sio, host="127.0.0.1", port=8000)
