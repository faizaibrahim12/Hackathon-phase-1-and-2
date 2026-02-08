"""
Additional API endpoint for signup with initial task creation
This endpoint registers a new user and creates an initial task in one request
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any
from ..auth.schemas import RegisterRequest, LoginResponse, UserResponse
from ..auth.service import AuthService
from ..tasks.schemas import TaskResponse
from ..tasks.service import TaskService
from ..database import get_session


router = APIRouter(prefix="/api", tags=["signup_with_task"])


@router.post("/signup-with-task", status_code=status.HTTP_201_CREATED)
async def signup_with_initial_task(
    request: RegisterRequest,
    initial_task_title: str = "Welcome Task",
    initial_task_description: str = "This is your first task after signing up!",
    session: Session = Depends(get_session),
) -> Dict[str, Any]:
    """
    Register a new user and create an initial task in one request
    
    Args:
        request: Registration request with email and password
        initial_task_title: Title for the initial task (optional)
        initial_task_description: Description for the initial task (optional)
        session: Database session
    
    Returns:
        Dictionary containing user info, token, and created task
    """
    # Register the new user
    user = AuthService.register(session, request.email, request.password)
    
    # Generate token for the newly registered user
    token_data = AuthService.login(session, request.email, request.password)
    
    # Create an initial task for the user
    initial_task = TaskService.create_task(
        session=session,
        user_id=str(user.id),  # Convert to string to match new Task model
        title=initial_task_title,
        description=initial_task_description,
        due_date=None
    )
    
    # Return comprehensive response
    response_data = {
        "user": UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
        ),
        "access_token": token_data["access_token"],
        "token_type": token_data["token_type"],
        "expires_in": token_data["expires_in"],
        "initial_task": TaskResponse(
            id=initial_task.id,
            user_id=initial_task.user_id,
            title=initial_task.title,
            description=initial_task.description,
            completed=initial_task.completed,
            due_date=initial_task.due_date,
            created_at=initial_task.created_at,
            updated_at=initial_task.updated_at,
        ),
        "message": f"User {request.email} registered successfully with initial task created!"
    }

    # Add refresh token if available
    if "refresh_token" in token_data:
        response_data["refresh_token"] = token_data["refresh_token"]

    return response_data


# Also add a simple test endpoint to demonstrate the functionality
@router.get("/demo-signup-task", status_code=status.HTTP_200_OK)
async def demo_signup_task_info() -> Dict[str, str]:
    """
    Informational endpoint about the signup with task functionality
    """
    return {
        "message": "Demo endpoint for signup with task creation",
        "endpoint": "/api/signup-with-task",
        "method": "POST",
        "description": "Register a new user and create an initial task in one request",
        "example_request_body": {
            "email": "newuser@example.com",
            "password": "securepassword123"
        },
        "example_query_params": {
            "initial_task_title": "Welcome Task",
            "initial_task_description": "This is your first task after signing up!"
        }
    }