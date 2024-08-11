# app/sockets.py
import socketio

# Initialize Socket.IO server instance
sio = socketio.AsyncServer(async_mode='asgi')
