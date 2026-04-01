"""Authentication Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AuthService
from app.auth.models import UserCreate, LoginRequest, AuthResponse, UserResponse
from app.core.dependencies import get_db
from app.core.exceptions import UserAlreadyExists, UserNotFound, AuthenticationError

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    try:
        user = await AuthService.register_user(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name,
            db=db
        )
        
        tokens = await AuthService.create_tokens(user.id)
        
        return AuthResponse(
            user=UserResponse.from_orm(user),
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
        )
    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=AuthResponse)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login user"""
    try:
        user = await AuthService.authenticate_user(
            email=credentials.email,
            password=credentials.password,
            db=db
        )
        
        tokens = await AuthService.create_tokens(user.id)
        
        return AuthResponse(
            user=UserResponse.from_orm(user),
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
        )
    except (UserNotFound, AuthenticationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail if hasattr(e, 'detail') else "Invalid credentials",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: dict = Depends(lambda: {"user_id": 1}),  # Placeholder
    db: AsyncSession = Depends(get_db)
):
    """Get current authenticated user"""
    try:
        user = await AuthService.get_user(current_user["user_id"], db=db)
        return UserResponse.from_orm(user)
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )
