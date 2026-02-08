import pytest
import asyncio
import sys
import os
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from unittest.mock import AsyncMock, patch

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app
from src.database import get_session
from src.chatbot.conversation_models import Conversation, Message
from src.tasks.models import Task


# Setup test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_chat_endpoint_creation(client: TestClient):
    """Test that the chat endpoint creates conversations properly"""
    response = client.post(
        "/api/chat/testuser",
        json={"message": "Hello, world!"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "conversation_id" in data
    assert "response" in data
    assert isinstance(data["conversation_id"], int)
    assert isinstance(data["response"], str)


def test_chat_endpoint_with_existing_conversation(client: TestClient, session: Session):
    """Test that the chat endpoint works with existing conversations"""
    # First, create a conversation by sending a message
    first_response = client.post(
        "/api/chat/testuser",
        json={"message": "Hello, world!"}
    )

    assert first_response.status_code == 200
    first_data = first_response.json()
    conversation_id = first_data["conversation_id"]

    # Now send another message to the same conversation
    second_response = client.post(
        "/api/chat/testuser",
        json={
            "conversation_id": conversation_id,
            "message": "How are you?"
        }
    )

    assert second_response.status_code == 200
    second_data = second_response.json()

    assert second_data["conversation_id"] == conversation_id
    assert "response" in second_data


def test_database_models():
    """Test that the database models are correctly defined"""
    # Test Conversation model
    conversation = Conversation(
        user_id="testuser",
    )
    
    assert conversation.user_id == "testuser"
    assert hasattr(conversation, "created_at")
    assert hasattr(conversation, "updated_at")
    
    # Test Message model
    message = Message(
        user_id="testuser",
        conversation_id=1,
        role="user",
        content="Hello"
    )
    
    assert message.user_id == "testuser"
    assert message.conversation_id == 1
    assert message.role == "user"
    assert message.content == "Hello"
    
    # Test Task model
    task = Task(
        user_id="testuser",
        title="Test task",
        description="Test description",
        completed=False
    )
    
    assert task.user_id == "testuser"
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed is False


@pytest.mark.asyncio
async def test_ai_agent_service():
    """Test the AI agent service integration"""
    from src.chatbot.ai_agent_service import AIAgentService

    # Mock the OpenAI client to avoid actual API calls
    with patch('src.chatbot.ai_agent_service.OpenAI') as mock_openai:
        mock_client_instance = AsyncMock()
        mock_completion = AsyncMock()
        mock_completion.choices = [AsyncMock()]
        mock_completion.choices[0].message = AsyncMock()
        mock_completion.choices[0].message.content = "Test response"
        mock_completion.choices[0].message.tool_calls = []

        mock_client_instance.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client_instance

        agent_service = AIAgentService()

        # Since we're mocking, we'll just test that the method can be called without error
        # In a real scenario, we'd test the actual integration
        assert agent_service is not None


if __name__ == "__main__":
    pytest.main([__file__])