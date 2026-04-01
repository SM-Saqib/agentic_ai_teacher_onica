"""WebSocket Event Definitions"""
from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class WSEvent:
    """Base WebSocket event"""
    type: str
    data: Any
    timestamp: Optional[str] = None


# Chat Events
@dataclass
class ChatMessageEvent(WSEvent):
    """Chat message event"""
    conversation_id: int
    content: str
    role: str = "user"


@dataclass
class ChatResponseEvent(WSEvent):
    """Chat response event"""
    conversation_id: int
    content: str
    thinking: bool = False


# Slide Events
@dataclass
class SlideSelectEvent(WSEvent):
    """Slide selection event"""
    slide_id: int


@dataclass
class SlideUpdateEvent(WSEvent):
    """Slide update event"""
    slide_id: int
    content: str


# Voice Events
@dataclass
class VoiceStartEvent(WSEvent):
    """Start voice recording event"""
    pass


@dataclass
class VoiceStopEvent(WSEvent):
    """Stop voice recording event"""
    audio_data: bytes


@dataclass
class VoiceTranscriptEvent(WSEvent):
    """Voice transcription result event"""
    transcript: str


# Avatar Events
@dataclass
class AvatarAnimateEvent(WSEvent):
    """Avatar animation event"""
    animation_type: str
    parameters: dict


# Connection Events
@dataclass
class ConnectionReadyEvent(WSEvent):
    """Connection established event"""
    user_id: int
    session_id: str


# Error Events
@dataclass
class ErrorEvent(WSEvent):
    """Error event"""
    error_code: str
    message: str
