"""Chat REST API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.service import ChatService
from app.api.schemas.chat import (
    ConversationCreate,
    ConversationResponse,
    ConversationDetailResponse,
    ConversationListResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    MessageResponse,
)
from app.core.dependencies import get_db
from app.core.exceptions import ConversationNotFound
from app.core.security import get_current_user

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    data: ConversationCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new conversation"""
    try:
        conversation = await ChatService.create_conversation(
            user_id=current_user["user_id"],
            slide_id=data.slide_id,
            title=data.title,
            db=db,
        )
        return ConversationResponse.from_orm(conversation)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all conversations for current user"""
    try:
        conversations = await ChatService.list_user_conversations(
            user_id=current_user["user_id"],
            limit=limit,
            db=db,
        )
        return ConversationListResponse(
            conversations=[ConversationResponse.from_orm(c) for c in conversations],
            total=len(conversations),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific conversation with messages"""
    try:
        conversation = await ChatService.get_conversation(
            conversation_id=conversation_id,
            user_id=current_user["user_id"],
            db=db,
        )
        messages = await ChatService.get_conversation_messages(
            conversation_id=conversation_id,
            db=db,
        )
        conv_data = ConversationResponse.from_orm(conversation)
        return ConversationDetailResponse(
            **conv_data.dict(),
            messages=[MessageResponse.from_orm(m) for m in messages],
        )
    except ConversationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Send a message and get a response"""
    try:
        # Verify conversation exists and belongs to user
        conversation = await ChatService.get_conversation(
            conversation_id=request.conversation_id,
            user_id=current_user["user_id"],
            db=db,
        )

        # Add user message
        user_msg = await ChatService.add_message(
            conversation_id=request.conversation_id,
            role="user",
            content=request.content,
            db=db,
        )

        # Get slide context if provided
        context = None
        if request.slide_id:
            context = await ChatService.get_slide_context(
                slide_id=request.slide_id,
                db=db,
            )

        # Generate response
        response_text, tokens_used = await ChatService.generate_response(
            question=request.content,
            conversation_id=request.conversation_id,
            context=context,
            db=db,
        )

        # Add assistant message
        assistant_msg = await ChatService.add_message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=response_text,
            tokens_used=tokens_used,
            db=db,
        )

        return ChatMessageResponse(
            message_id=assistant_msg.id,
            conversation_id=request.conversation_id,
            user_message=request.content,
            assistant_message=response_text,
            tokens_used=tokens_used,
            created_at=assistant_msg.created_at,
        )

    except ConversationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation"""
    try:
        conversation = await ChatService.get_conversation(
            conversation_id=conversation_id,
            user_id=current_user["user_id"],
            db=db,
        )
        await db.delete(conversation)
        await db.commit()
    except ConversationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
