#!/usr/bin/env python3
"""
Test script to simulate signup and task creation
This script will:
1. Create a new user via signup
2. Create a task for that user
3. Save both to the database
"""

import asyncio
from sqlmodel import Session, select
from datetime import datetime
from src.database import engine, get_session
from src.auth.models import User
from src.auth.service import AuthService
from src.tasks.models import Task
from src.tasks.service import TaskService
from src.config import settings


def test_signup_and_task_creation():
    """Test signup and task creation functionality"""
    
    print("Starting signup and task creation test...")
    
    # Create a database session
    with Session(engine) as session:
        # Step 1: Simulate signup by creating a new user
        email = "testuser@example.com"
        password = "securepassword123"
        
        print(f"Creating user with email: {email}")
        
        try:
            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == email)).first()
            if existing_user:
                print(f"User {email} already exists, deleting for clean test...")
                session.delete(existing_user)
                session.commit()
            
            # Create new user (this simulates the signup process)
            new_user = AuthService.register(session, email, password)
            session.refresh(new_user)  # Refresh to get the auto-generated ID
            
            print(f"[SUCCESS] User created successfully with ID: {new_user.id}")
            print(f"  Email: {new_user.email}")
            print(f"  Created at: {new_user.created_at}")
            
            # Step 2: Create a task for the new user
            task_title = "Signup Test Task"
            task_description = "This task was created after successful signup to test database save functionality."
            
            print(f"\nCreating task: '{task_title}' for user ID: {new_user.id}")
            
            new_task = TaskService.create_task(
                session=session,
                user_id=new_user.id,
                title=task_title,
                description=task_description,
                due_date=None  # No due date for this test
            )
            
            session.refresh(new_task)  # Refresh to get the auto-generated ID
            
            print(f"[SUCCESS] Task created successfully with ID: {new_task.id}")
            print(f"  Title: {new_task.title}")
            print(f"  Description: {new_task.description}")
            print(f"  User ID: {new_task.user_id}")
            print(f"  Created at: {new_task.created_at}")
            
            # Step 3: Verify data was saved by querying the database
            print("\nVerifying saved data...")
            
            # Query the user
            saved_user = session.exec(select(User).where(User.id == new_user.id)).first()
            if saved_user:
                print(f"[SUCCESS] User verified in database: {saved_user.email}")
            else:
                print("[ERROR] User not found in database")
                
            # Query the task
            saved_task = session.exec(select(Task).where(Task.id == new_task.id)).first()
            if saved_task:
                print(f"[SUCCESS] Task verified in database: {saved_task.title}")
                print(f"  Belongs to user ID: {saved_task.user_id}")
            else:
                print("[ERROR] Task not found in database")
            
            # Show all tasks for this user
            user_tasks = session.exec(select(Task).where(Task.user_id == new_user.id)).all()
            print(f"\nTotal tasks for user {new_user.id}: {len(user_tasks)}")
            
            print("\n[COMPLETE] Signup and task creation test completed successfully!")
            print(f"User '{email}' was created and a test task was saved to the database.")
            
        except Exception as e:
            print(f"[ERROR] Error during signup/task creation: {str(e)}")
            session.rollback()


def view_database_contents():
    """View current database contents for debugging"""
    print("\nCurrent database contents:")
    
    with Session(engine) as session:
        # Count users
        users = session.exec(select(User)).all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"  - ID: {user.id}, Email: {user.email}, Created: {user.created_at}")
        
        # Count tasks
        tasks = session.exec(select(Task)).all()
        print(f"Total tasks: {len(tasks)}")
        for task in tasks:
            print(f"  - ID: {task.id}, Title: {task.title}, User ID: {task.user_id}, Completed: {task.completed}")


if __name__ == "__main__":
    print("=== Signup and Task Creation Test ===")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Environment: {settings.ENVIRONMENT}")
    
    # View initial database state
    print("\nInitial database state:")
    view_database_contents()
    
    # Run the test
    test_signup_and_task_creation()
    
    # View final database state
    print("\nFinal database state:")
    view_database_contents()
    
    print("\nTest completed!")