"""WebSocket Manager - handles connection management and message routing"""
import json
import logging
from typing import Callable, Dict, Set
from fastapi import WebSocket, WebSocketDisconnect, status

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections and message broadcasting"""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[int, Set[str]] = {}  # user_id -> set of connection ids
        self.message_handlers: Dict[str, Callable] = {}

    async def connect(self, connection_id: str, websocket: WebSocket, user_id: int) -> None:
        """Register a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(connection_id)
        
        logger.info(f"Client {connection_id} connected (user_id: {user_id})")

    def disconnect(self, connection_id: str, user_id: int) -> None:
        """Remove a WebSocket connection"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        if user_id in self.user_connections:
            self.user_connections[user_id].discard(connection_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        logger.info(f"Client {connection_id} disconnected (user_id: {user_id})")

    async def broadcast(self, message: dict) -> None:
        """Broadcast message to all connected clients"""
        for connection_id, websocket in list(self.active_connections.items()):
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {connection_id}: {e}")
                self.disconnect(connection_id, None)

    async def broadcast_to_user(self, user_id: int, message: dict) -> None:
        """Broadcast message to all connections of a specific user"""
        if user_id not in self.user_connections:
            return
        
        for connection_id in list(self.user_connections[user_id]):
            try:
                websocket = self.active_connections.get(connection_id)
                if websocket:
                    await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error sending to {connection_id}: {e}")

    async def send_personal(self, connection_id: str, message: dict) -> None:
        """Send message to a specific connection"""
        websocket = self.active_connections.get(connection_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error sending personal message to {connection_id}: {e}")

    def register_handler(self, event_type: str, handler: Callable) -> None:
        """Register a message handler for an event type"""
        self.message_handlers[event_type] = handler

    async def handle_message(self, event_type: str, data: dict, user_id: int) -> None:
        """Route message to appropriate handler"""
        handler = self.message_handlers.get(event_type)
        if handler:
            try:
                await handler(data, user_id)
            except Exception as e:
                logger.error(f"Error handling event {event_type}: {e}")
                raise


# Global manager instance
manager = WebSocketManager()
