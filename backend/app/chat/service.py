"""Chat Service - Core chat logic and message handling"""
import logging
from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import Conversation, Message, Slide
from app.core.exceptions import ConversationNotFound, SlideNotFound
from app.llm.client import llm_client
from app.llm.prompts import format_chat_prompt
from app.config.constants import DEFAULT_CHAT_MAX_TOKENS, DEFAULT_CHAT_TEMPERATURE

logger = logging.getLogger(__name__)


class ChatService:
    """Service for chat operations"""

    @staticmethod
    async def create_conversation(
        user_id: int,
        slide_id: Optional[int] = None,
        title: Optional[str] = None,
        db: AsyncSession = None,
    ) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            user_id=user_id,
            slide_id=slide_id,
            title=title or "New Conversation",
        )

        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

        logger.info(f"Created conversation {conversation.id} for user {user_id}")
        return conversation

    @staticmethod
    async def get_conversation(
        conversation_id: int,
        user_id: int,
        db: AsyncSession = None,
    ) -> Conversation:
        """Get a conversation by ID (with user verification)"""
        result = await db.execute(
            select(Conversation).where(
                (Conversation.id == conversation_id) & (Conversation.user_id == user_id)
            )
        )
        conversation = result.scalars().first()

        if not conversation:
            raise ConversationNotFound(conversation_id)

        return conversation

    @staticmethod
    async def get_conversation_messages(
        conversation_id: int,
        limit: int = 100,
        db: AsyncSession = None,
    ) -> List[Message]:
        """Get messages from a conversation"""
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        # Reverse to get chronological order
        return list(reversed(messages))

    @staticmethod
    async def add_message(
        conversation_id: int,
        role: str,
        content: str,
        tokens_used: Optional[int] = None,
        db: AsyncSession = None,
    ) -> Message:
        """Add a message to a conversation"""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tokens_used=tokens_used,
        )

        db.add(message)
        await db.commit()
        await db.refresh(message)

        return message

    @staticmethod
    async def get_slide_context(
        slide_id: int,
        db: AsyncSession = None,
    ) -> Optional[str]:
        """Get slide content as context for chat"""
        result = await db.execute(
            select(Slide).where(Slide.id == slide_id)
        )
        slide = result.scalars().first()

        if not slide:
            return None

        # Combine title and content as context
        context = f"Title: {slide.title}\n\n{slide.content}"
        if slide.description:
            context += f"\n\nDescription: {slide.description}"

        return context

    @staticmethod
    async def generate_response(
        question: str,
        conversation_id: int,
        context: Optional[str] = None,
        temperature: float = DEFAULT_CHAT_TEMPERATURE,
        max_tokens: int = DEFAULT_CHAT_MAX_TOKENS,
        db: AsyncSession = None,
    ) -> Tuple[str, Optional[int]]:
        """Generate an AI response to a question"""
        try:
            # Get conversation history
            messages = await ChatService.get_conversation_messages(
                conversation_id,
                limit=5,
                db=db,
            )

            # Format as dict for prompt
            message_dicts = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            # Format the prompt with context
            prompt = format_chat_prompt(
                question=question,
                context=context,
                conversation_history=message_dicts,
            )

            # Generate response from LLM
            logger.info(f"Generating response for conversation {conversation_id}")
            response = await llm_client.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Calculate approximate tokens (rough estimation)
            tokens_used = len(response.split()) + len(question.split())

            return response, tokens_used

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    @staticmethod
    async def stream_response(
        question: str,
        conversation_id: int,
        context: Optional[str] = None,
        temperature: float = DEFAULT_CHAT_TEMPERATURE,
        max_tokens: int = DEFAULT_CHAT_MAX_TOKENS,
        db: AsyncSession = None,
    ):
        """Stream an AI response (for WebSocket)"""
        try:
            # Get conversation history
            messages = await ChatService.get_conversation_messages(
                conversation_id,
                limit=5,
                db=db,
            )

            # Format as dict for prompt
            message_dicts = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            # Format the prompt with context
            prompt = format_chat_prompt(
                question=question,
                context=context,
                conversation_history=message_dicts,
            )

            # Stream response from LLM
            logger.info(f"Streaming response for conversation {conversation_id}")
            async for chunk in llm_client.stream_generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            ):
                yield chunk

        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise

    @staticmethod
    async def update_conversation_context(
        conversation_id: int,
        context: str,
        db: AsyncSession = None,
    ) -> Conversation:
        """Update the context field of a conversation"""
        conversation = await db.get(Conversation, conversation_id)
        if not conversation:
            raise ConversationNotFound(conversation_id)

        conversation.context = context
        await db.commit()
        await db.refresh(conversation)

        return conversation

    @staticmethod
    async def list_user_conversations(
        user_id: int,
        limit: int = 20,
        db: AsyncSession = None,
    ) -> List[Conversation]:
        """Get all conversations for a user"""
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
