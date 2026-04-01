"""WebSocket Middleware and Utilities"""
import uuid
import logging
from fastapi import WebSocket, HTTPException, status
from app.core.security import verify_token

logger = logging.getLogger(__name__)


async def validate_websocket_token(websocket: WebSocket, token: str) -> dict:
    """Validate JWT token for WebSocket connection"""
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")
        return {"user_id": int(user_id)}
    except Exception as e:
        logger.error(f"WebSocket auth error: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e


def generate_connection_id() -> str:
    """Generate unique connection ID"""
    return str(uuid.uuid4())
