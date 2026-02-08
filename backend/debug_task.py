import asyncio
import sys
from sqlmodel import Session
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, './src')

from src.database import get_session
from src.tasks.service import TaskService
from src.tasks.models import Task

async def debug_task_creation():
    print("Starting task creation debug...")
    
    # Get a session
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Try to create a task directly using the service
        print("Attempting to create task via TaskService...")
        task = TaskService.create_task(
            session=session,
            user_id="50",  # Using the user_id from the previous login
            title="Debug task",
            description="Task for debugging purposes"
        )
        
        print(f"Task created successfully: {task.id}, {task.title}, {task.user_id}")
        
        # Now try to convert it to a response object to check serialization
        from src.tasks.schemas import TaskResponse
        
        print("Attempting to serialize task to TaskResponse...")
        response = TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        
        print(f"Serialization successful: {response}")
        print(f"Response dict: {response.model_dump()}")
        
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        session.close()

if __name__ == "__main__":
    asyncio.run(debug_task_creation())