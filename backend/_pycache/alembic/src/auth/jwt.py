"""JWT token creation and verification utilities"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from ..config import settings


def create_access_token(user_id: int, email: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate JWT access token for user

    Args:
        user_id: User ID to encode in token
        email: User email to encode in token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = {
        "sub": str(user_id),
        "email": email,
    }

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.effective_jwt_secret,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode JWT token

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload if valid, None otherwise

    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        # Ensure we're using the same secret that was used to encode
        payload = jwt.decode(
            token,
            settings.effective_jwt_secret,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError as e:
        # Log the specific error for debugging
        print(f"JWT Error: {e}")
        return None
    except Exception as e:
        # Log any other errors
        print(f"Unexpected error during JWT verification: {e}")
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user ID from valid JWT token

    Args:
        token: JWT token string

    Returns:
        User ID if token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload is None:
        return None

    try:
        user_id = int(payload.get("sub"))
        return user_id
    except (ValueError, TypeError):
        return None
