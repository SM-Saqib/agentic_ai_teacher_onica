"""WebSocket Routes for Chat"""
import uuid
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.websocket.manager import manager
from app.websocket.middleware import validate_websocket_token, generate_connection_id
from app.websocket.handlers import register_chat_handlers
from app.core.dependencies import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws/v1", tags=["websocket"])

# Register handlers on module load
register_chat_handlers()


@router.websocket("/chat/{token}")
async def chat_websocket(
    websocket: WebSocket,
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """WebSocket endpoint for chat"""
    connection_id = generate_connection_id()
    user_id = None
    
    try:
        # Validate token and extract user info
        user_info = await validate_websocket_token(websocket, token)
        user_id = user_info["user_id"]
        
        # Register connection
        await manager.connect(connection_id, websocket, user_id)
        
        # Send connection ready event
        await manager.send_personal(connection_id, {
            "event": "connection.ready",
            "data": {"user_id": user_id, "connection_id": connection_id}
        })
        
        logger.info(f"Chat WebSocket connected for user {user_id}")
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            event_type = data.get("event")
            event_data = data.get("data", {})
            
            logger.info(f"Received event {event_type} from user {user_id}")
            
            # Route to handler
            try:
                await manager.handle_message(event_type, event_data, user_id)
            except Exception as e:
                logger.error(f"Error handling event: {e}")
                await manager.send_personal(connection_id, {
                    "event": "error",
                    "data": {"message": str(e)}
                })
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {connection_id}")
        if user_id:
            manager.disconnect(connection_id, user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if connection_id in manager.active_connections:
            manager.disconnect(connection_id, user_id if user_id else None)

