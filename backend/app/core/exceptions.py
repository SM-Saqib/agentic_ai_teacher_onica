"""Custom exceptions for the application"""
from fastapi import HTTPException, status


class AITeacherException(Exception):
    """Base exception for AI Teacher application"""
    pass


class AuthenticationError(AITeacherException):
    """Raised when authentication fails"""
    def __init__(self, detail: str = "Authentication failed"):
        self.detail = detail


class UserNotFound(AITeacherException):
    """Raised when user is not found"""
    def __init__(self, user_id: str):
        self.detail = f"User {user_id} not found"


class UserAlreadyExists(AITeacherException):
    """Raised when trying to create a user that already exists"""
    def __init__(self, email: str):
        self.detail = f"User with email {email} already exists"


class InvalidToken(AITeacherException):
    """Raised when token is invalid"""
    def __init__(self, detail: str = "Invalid or expired token"):
        self.detail = detail


class SlideNotFound(AITeacherException):
    """Raised when slide is not found"""
    def __init__(self, slide_id: str):
        self.detail = f"Slide {slide_id} not found"


class ConversationNotFound(AITeacherException):
    """Raised when conversation is not found"""
    def __init__(self, conversation_id: str):
        self.detail = f"Conversation {conversation_id} not found"


class LLMError(AITeacherException):
    """Raised when LLM API call fails"""
    def __init__(self, detail: str = "LLM service error"):
        self.detail = detail


class VectorStoreError(AITeacherException):
    """Raised when vector store operation fails"""
    def __init__(self, detail: str = "Vector store error"):
        self.detail = detail


class DatabaseError(AITeacherException):
    """Raised when database operation fails"""
    def __init__(self, detail: str = "Database error"):
        self.detail = detail


# HTTP exception converters
def auth_exception_to_http(exc: AuthenticationError) -> HTTPException:
    """Convert AuthenticationError to HTTPException"""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exc.detail,
    )


def not_found_exception_to_http(detail: str) -> HTTPException:
    """Convert not found exception to HTTPException"""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
    )


def conflict_exception_to_http(detail: str) -> HTTPException:
    """Convert conflict exception to HTTPException"""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
    )
