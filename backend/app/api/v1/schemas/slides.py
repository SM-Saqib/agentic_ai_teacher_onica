"""Pydantic schemas for slides API"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SlideCreate(BaseModel):
    """Schema for creating a slide"""
    title: str
    content: str
    description: Optional[str] = None
    is_prebuilt: bool = True
    version: int = 1


class SlideResponse(BaseModel):
    """Schema for slide response"""
    id: int
    title: str
    content: str
    description: Optional[str] = None
    is_prebuilt: bool
    version: int
    embedding_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SlideExplanationCreate(BaseModel):
    """Schema for creating a slide explanation"""
    explanation: str
    language: str = "en"


class SlideExplanationResponse(BaseModel):
    """Schema for slide explanation response"""
    id: int
    slide_id: int
    explanation: str
    language: str
    embedding_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True