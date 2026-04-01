"""WebSocket Event Handlers for Chat"""
import logging
import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.service import ChatService
from app.websocket.manager import manager
from app.config.constants import DEFAULT_CHAT_MAX_TOKENS, DEFAULT_CHAT_TEMPERATURE
from app.core.exceptions import ConversationNotFound

logger = logging.getLogger(__name__)


async def handle_chat_message(data: dict, user_id: int, db: AsyncSession = None):
    """Handle chat.message event"""
    try:
        conversation_id = data.get("conversation_id")
        content = data.get("content")
        slide_id = data.get("slide_id")

        if not conversation_id or not content:
            await manager.broadcast_to_user(user_id, {
                "event": "error",
                "data": {"message": "Missing required fields"}
            })
            return

        # Verify conversation belongs to user
        conversation = await ChatService.get_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            db=db,
        )

        # Add user message
        user_msg = await ChatService.add_message(
            conversation_id=conversation_id,
            role="user",
            content=content,
            db=db,
        )

        # Send confirmation
        await manager.broadcast_to_user(user_id, {
            "event": "chat.user_message",
            "data": {
                "message_id": user_msg.id,
                "conversation_id": conversation_id,
                "content": content,
            }
        })

        # Get slide context if provided
        context = None
        if slide_id:
            context = await ChatService.get_slide_context(
                slide_id=slide_id,
                db=db,
            )

        # Stream response
        full_response = ""
        async for chunk in ChatService.stream_response(
            question=content,
            conversation_id=conversation_id,
            context=context,
            temperature=DEFAULT_CHAT_TEMPERATURE,
            max_tokens=DEFAULT_CHAT_MAX_TOKENS,
            db=db,
        ):
            full_response += chunk
            # Send chunk to user
            await manager.broadcast_to_user(user_id, {
                "event": "chat.response_chunk",
                "data": {
                    "conversation_id": conversation_id,
                    "chunk": chunk,
                }
            })

        # Save complete response
        tokens_used = len(full_response.split()) + len(content.split())
        assistant_msg = await ChatService.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_response,
            tokens_used=tokens_used,
            db=db,
        )

        # Send completion
        await manager.broadcast_to_user(user_id, {
            "event": "chat.response_complete",
            "data": {
                "message_id": assistant_msg.id,
                "conversation_id": conversation_id,
                "tokens_used": tokens_used,
            }
        })

    except ConversationNotFound as e:
        logger.error(f"Conversation not found: {e}")
        await manager.broadcast_to_user(user_id, {
            "event": "error",
            "data": {"message": "Conversation not found"}
        })
    except Exception as e:
        logger.error(f"Error handling chat message: {e}")
        await manager.broadcast_to_user(user_id, {
            "event": "error",
            "data": {"message": str(e)}
        })


async def handle_chat_follow_up(data: dict, user_id: int, db: AsyncSession = None):
    """Handle chat.follow_up event (follow-up question)"""
    # Same as chat message
    await handle_chat_message(data, user_id, db)


async def handle_conversation_create(data: dict, user_id: int, db: AsyncSession = None):
    """Handle conversation.create event"""
    try:
        title = data.get("title")
        slide_id = data.get("slide_id")

        conversation = await ChatService.create_conversation(
            user_id=user_id,
            slide_id=slide_id,
            title=title,
            db=db,
        )

        await manager.broadcast_to_user(user_id, {
            "event": "conversation.created",
            "data": {
                "conversation_id": conversation.id,
                "title": conversation.title,
                "slide_id": conversation.slide_id,
            }
        })

    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        await manager.broadcast_to_user(user_id, {
            "event": "error",
            "data": {"message": str(e)}
        })


# Register handlers
def register_chat_handlers():
    """Register all chat event handlers"""
    manager.register_handler("chat.message", handle_chat_message)
    manager.register_handler("chat.follow_up", handle_chat_follow_up)
    manager.register_handler("conversation.create", handle_conversation_create)
    logger.info("Chat handlers registered")
