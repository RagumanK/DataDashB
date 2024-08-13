import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import orders
from app.db.init_db import init_db
from app.core.sockets import sio_app  # Import sio from the sockets module

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing purposes, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the orders router
app.include_router(orders.router, prefix="/api/v1")

app.mount('/', sio_app)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get('/')
async def home():
    return {'message': 'Hello👋 Developers💻'}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
