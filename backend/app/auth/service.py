"""Authentication Service"""
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import User, UserSession
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.exceptions import UserNotFound, UserAlreadyExists, AuthenticationError


class AuthService:
    """Handle user authentication operations"""

    @staticmethod
    async def register_user(
        email: str,
        username: str,
        password: str,
        full_name: str = None,
        db: AsyncSession = None
    ) -> User:
        """Register a new user"""
        # Check if user already exists
        result = await db.execute(
            select(User).where((User.email == email) | (User.username == username))
        )
        existing_user = result.scalars().first()
        
        if existing_user:
            if existing_user.email == email:
                raise UserAlreadyExists(email)
            raise UserAlreadyExists(username)

        # Create new user
        hashed_password = hash_password(password)
        new_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user

    @staticmethod
    async def authenticate_user(
        email: str,
        password: str,
        db: AsyncSession = None
    ) -> User:
        """Authenticate user with email and password"""
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if not user:
            raise UserNotFound(email)
        
        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")
        
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
        
        return user

    @staticmethod
    async def create_tokens(user_id: int) -> dict:
        """Create access and refresh tokens for user"""
        access_token = create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(minutes=30)
        )
        refresh_token = create_refresh_token(data={"sub": str(user_id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 30 * 60,  # 30 minutes in seconds
        }

    @staticmethod
    async def get_user(user_id: int, db: AsyncSession = None) -> User:
        """Get user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        
        if not user:
            raise UserNotFound(user_id)
        
        return user
