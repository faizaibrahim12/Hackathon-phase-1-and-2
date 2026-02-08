"""Authentication API routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlmodel import Session
from datetime import datetime, timedelta
from .schemas import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    LoginResponse,
)
from .service import AuthService
from .jwt import get_user_id_from_token, create_access_token
from ..database import get_session
from ..exceptions import InvalidTokenException
from .refresh_token_model import RefreshToken, generate_refresh_token, get_default_refresh_token_expiry
from jose import JWTError, jwt

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_session),
) -> LoginResponse:
    """
    Register a new user and return JWT token
netstat -ano | findstr :3001
    Args:
        request: Registration request with email and password
        session: Database session

    Returns:
        LoginResponse with access_token and user info
        curl -v -X POST http://127.0.0.1:8000/api/auth/register \
      -H "Content-Type: application/json" \
      -d '{"email":"me+test@example.com","password":"Passw0rd1"}'"""
    user = AuthService.register(session, request.email, request.password)

    # Generate token for the newly registered user
    token_data = AuthService.login(session, request.email, request.password)

    return LoginResponse(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        refresh_token=token_data.get("refresh_token"),
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
        ),
    )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    session: Session = Depends(get_session),
) -> LoginResponse:
    """
    Login user and receive JWT token

    Args:
        request: Login request with email and password
        session: Database session

    Returns:
        LoginResponse with access_token and user info
    """
    token_data = AuthService.login(session, request.email, request.password)
    user = AuthService.get_user_by_email(session, request.email)

    return LoginResponse(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        refresh_token=token_data.get("refresh_token"),
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
        ),
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
) -> dict:
    """
    Logout user (invalidate token on client side)

    Note: Token invalidation is handled on the client side by removing
    the token from storage. This endpoint is provided for completeness.

    Args:
        request: HTTP request (contains user_id from middleware)

    Returns:
        Success message
    """
    # The middleware has already validated the token
    # In a real implementation, you might want to invalidate the refresh token here
    return {"message": "Logged out successfully"}


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(
    request_body: dict,
    session: Session = Depends(get_session),
) -> LoginResponse:
    """
    Refresh an expired access token using a refresh token

    Args:
        request_body: Request body containing refresh_token
        session: Database session

    Returns:
        LoginResponse with new access_token and user info
    """
    refresh_token_str = request_body.get("refresh_token")
    
    if not refresh_token_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required"
        )
    
    # Look up the refresh token in the database
    from sqlmodel import select
    refresh_token_obj = session.exec(
        select(RefreshToken).where(RefreshToken.token == refresh_token_str)
    ).first()
    
    if not refresh_token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if refresh token has expired
    if refresh_token_obj.expires_at < datetime.utcnow():
        session.delete(refresh_token_obj)
        session.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    
    # Get user associated with the refresh token
    user = AuthService.get_user_by_id(session, refresh_token_obj.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Generate new access token
    new_access_token = create_access_token(user.id, user.email)
    
    # Generate new refresh token
    new_refresh_token_str = generate_refresh_token()
    
    # Delete old refresh token and create new one
    session.delete(refresh_token_obj)
    new_refresh_token_obj = RefreshToken(
        token=new_refresh_token_str,
        user_id=user.id,
        expires_at=get_default_refresh_token_expiry()
    )
    session.add(new_refresh_token_obj)
    session.commit()
    
    return LoginResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=604800,
        refresh_token=new_refresh_token_str,
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
        ),
    )


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> UserResponse:
    """
    Get current authenticated user info

    Args:
        request: HTTP request (contains user_id from middleware)
        session: Database session

    Returns:
        UserResponse with current user info

    Raises:
        InvalidTokenException: If token is missing or invalid
    """
    # Get user_id from the middleware (which validates the token)
    user_id = getattr(request.state, 'user_id', None)
    if user_id is None:
        raise InvalidTokenException()

    # Get user from database
    user = AuthService.get_user_by_id(session, user_id)
    if user is None:
        raise InvalidTokenException()

    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
    )


[{'e}': 'pass\n\n    # If not in body', 'refresh_token': 'refresh_token = request.headers.get(', 'X-Refresh-Token': 'if not refresh_token:\n        print(', 'DEBUG': 'No refresh token found', 'print(f': 'EBUG: Looking for refresh token in database: {refresh_token'}, {'token_type="bearer': 'expires_in=3600'}]
