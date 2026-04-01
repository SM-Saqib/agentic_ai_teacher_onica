"""SQLAlchemy ORM Models"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.database.connection import Base

# Many-to-many association tables
message_entities = Table(
    'message_entities',
    Base.metadata,
    Column('message_id', Integer, ForeignKey('messages.id'), primary_key=True),
    Column('entity_id', Integer, ForeignKey('knowledge_entities.id'), primary_key=True),
)


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    tier = Column(String(50), default="free")  # free, premium, enterprise
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    avatar_config = relationship("AvatarConfig", back_populates="user", uselist=False)


class UserSession(Base):
    """User session tokens"""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(500), nullable=False)
    refresh_token = Column(String(500))
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_revoked = Column(Boolean, default=False)


class Slide(Base):
    """Slide model"""
    __tablename__ = "slides"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    description = Column(Text)
    is_prebuilt = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    embedding_id = Column(String(255))  # Reference to vector store
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    explanations = relationship("SlideExplanation", back_populates="slide", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="slide")


class SlideExplanation(Base):
    """Pre-built explanations for slides"""
    __tablename__ = "slide_explanations"

    id = Column(Integer, primary_key=True, index=True)
    slide_id = Column(Integer, ForeignKey("slides.id"), nullable=False)
    explanation = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    embedding_id = Column(String(255))  # Reference to vector store
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    slide = relationship("Slide", back_populates="explanations")


class Conversation(Base):
    """Chat conversation"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    slide_id = Column(Integer, ForeignKey("slides.id"), nullable=True)
    title = Column(String(255))
    context = Column(Text)  # Stored conversation context
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    slide = relationship("Slide", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Chat message"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class KnowledgeEntity(Base):
    """Knowledge base entities"""
    __tablename__ = "knowledge_entities"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    source_type = Column(String(50))  # "slide", "explanation", "external"
    source_id = Column(Integer)
    embedding_id = Column(String(255))  # Reference to vector store
    created_at = Column(DateTime, default=datetime.utcnow)


class VoiceLog(Base):
    """Voice interaction logs"""
    __tablename__ = "voice_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transcription = Column(Text)
    duration_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class AvatarConfig(Base):
    """User avatar configuration"""
    __tablename__ = "avatar_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    avatar_type = Column(String(50))  # "basic", "premium", "enterprise"
    model_id = Column(String(255))
    settings = Column(Text)  # JSON stored as text
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="avatar_config")
