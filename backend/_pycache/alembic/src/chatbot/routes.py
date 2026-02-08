from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import Optional
from ..database import get_session
from ..chatbot.conversation_models import Conversation, Message, ConversationCreate, MessageCreate
from ..chatbot.ai_agent_service import AIAgentService
from datetime import datetime
import uuid

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("")
async def chat(
    request: Request,
    conversation_id: Optional[int] = None,
    message: str = "",
    session: Session = Depends(get_session)
):
    # Extract authenticated user_id from request state and convert to string
    user_id = str(request.state.user_id)
    """
    Chat endpoint that receives user messages and returns AI responses.
    Maintains conversation state in the database.
    """
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content is required"
        )

    # Get or create conversation
    if conversation_id:
        # Check if conversation exists and belongs to user
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation_data = ConversationCreate(user_id=user_id)
        conversation = Conversation.from_orm(conversation_data) if hasattr(Conversation, 'from_orm') else Conversation(**conversation_data.dict())
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        conversation_id = conversation.id

    # Store user message in database
    user_message = MessageCreate(
        user_id=user_id,
        conversation_id=conversation_id,
        role="user",
        content=message
    )
    db_user_message = Message.from_orm(user_message) if hasattr(Message, 'from_orm') else Message(**user_message.dict())
    session.add(db_user_message)
    session.commit()

    # Process with AI agent
    agent_service = AIAgentService()
    result = await agent_service.process_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=user_id,
        user_message=message
    )

    ai_response = result["response"]
    tool_calls = result["tool_calls"]

    # Store AI response in database
    ai_message = MessageCreate(
        user_id=user_id,
        conversation_id=conversation_id,
        role="assistant",
        content=ai_response
    )
    db_ai_message = Message.from_orm(ai_message) if hasattr(Message, 'from_orm') else Message(**ai_message.dict())
    session.add(db_ai_message)
    session.commit()

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()

    return {
        "conversation_id": conversation_id,
        "response": ai_response,
        "tool_calls": tool_calls
    }