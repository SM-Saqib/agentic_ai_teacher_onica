"""Chat API Schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MessageBase(BaseModel):
    """Base message schema"""
    role: str
    content: str


class MessageCreate(MessageBase):
    """Create message schema"""
    pass


class MessageResponse(MessageBase):
    """Message response schema"""
    id: int
    conversation_id: int
    tokens_used: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    """Base conversation schema"""
    title: Optional[str] = None
    slide_id: Optional[int] = None


class ConversationCreate(ConversationBase):
    """Create conversation schema"""
    pass


class ConversationResponse(ConversationBase):
    """Conversation response schema"""
    id: int
    user_id: int
    context: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationDetailResponse(ConversationResponse):
    """Conversation with messages"""
    messages: List[MessageResponse] = []


class ChatMessageRequest(BaseModel):
    """Chat message request"""
    conversation_id: int
    content: str = Field(..., min_length=1, max_length=5000)
    slide_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Chat message response"""
    message_id: int
    conversation_id: int
    user_message: str
    assistant_message: str
    tokens_used: Optional[int] = None
    created_at: datetime


class ChatStreamRequest(BaseModel):
    """Chat stream request for WebSocket"""
    event: str = "chat.message"
    data: ChatMessageRequest


class ChatStreamResponse(BaseModel):
    """Chat stream response for WebSocket"""
    event: str
    data: dict


class ConversationListResponse(BaseModel):
    """List of conversations"""
    conversations: List[ConversationResponse]
    total: int
