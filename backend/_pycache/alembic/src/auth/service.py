"""Authentication business logic service"""
from sqlmodel import Session, select
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from .models import User
from .security import hash_password, verify_password
from .jwt import create_access_token
from ..exceptions import (
    InvalidCredentialsException,
    EmailAlreadyExistsException,
)
from .refresh_token_model import RefreshToken, generate_refresh_token, get_default_refresh_token_expiry


class AuthService:
    """Service for authentication operations"""

    @staticmethod
    def register(session: Session, email: str, password: str) -> User:
        """
        Register a new user

        Args:
            session: Database session
            email: User email
            password: Plain text password

        Returns:
            Created User object

        Raises:
            EmailAlreadyExistsException: If email already registered
        """
        # Check if email already exists
        existing_user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if existing_user:
            raise EmailAlreadyExistsException()

        # Validate password length (max 72 chars due to bcrypt limitation)
        if len(password) < 8 or len(password) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "invalid_password",
                    "detail": "Password must be between 8 and 72 characters"
                }
            )

        # Hash password and create user
        hashed_password = hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Create a welcome task for the new user
        # Import here to avoid circular imports
        from ..tasks.service import TaskService
        TaskService.create_task(
            session=session,
            user_id=user.id,
            title="Welcome to the Task App!",
            description=f"Congratulations {user.email}, you've successfully signed up! This is your first task.",
        )

        return user

    @staticmethod
    def login(session: Session, email: str, password: str) -> dict:
        """
        Authenticate user and return JWT token

        Args:
            session: Database session
            email: User email
            password: Plain text password

        Returns:
            Dictionary with access_token, token_type, expires_in, and refresh_token

        Raises:
            InvalidCredentialsException: If credentials are incorrect
        """
        # Find user by email
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user:
            raise InvalidCredentialsException()

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()

        # Generate JWT token
        access_token = create_access_token(user.id, user.email)

        # Generate refresh token
        refresh_token_str = generate_refresh_token()
        refresh_token_obj = RefreshToken(
            token=refresh_token_str,
            user_id=user.id,
            expires_at=get_default_refresh_token_expiry()
        )
        session.add(refresh_token_obj)
        session.commit()

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 604800,  # 7 days in seconds
            "refresh_token": refresh_token_str
        }

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> User | None:
        """
        Get user by ID

        Args:
            session: Database session
            user_id: User ID

        Returns:
            User object if found, None otherwise
        """
        return session.exec(
            select(User).where(User.id == user_id)
        ).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> User | None:
        """
        Get user by email

        Args:
            session: Database session
            email: User email

        Returns:
            User object if found, None otherwise
        """
        return session.exec(
            select(User).where(User.email == email)
        ).first()
