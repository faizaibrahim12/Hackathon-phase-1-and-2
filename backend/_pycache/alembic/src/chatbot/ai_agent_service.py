import asyncio
from typing import Dict, Any, List
from openai import OpenAI
from sqlmodel import Session, select
from .conversation_models import Message
from ..config import settings
import json


class AIAgentService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)  # Need to add this to config
    
    async def process_conversation(
        self,
        session: Session,
        conversation_id: int,
        user_id: str,
        user_message: str
    ) -> Dict[str, Any]:
        """
        Process a user message using OpenAI Agent with MCP tools
        """
        # Retrieve conversation history
        messages_db = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()
        
        # Convert to OpenAI format
        conversation_history = []
        for msg in messages_db:
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add the new user message
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Define tools that correspond to MCP tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description (optional)"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "status": {"type": "string", "description": "Filter by status: all, pending, completed (optional)"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "task_id": {"type": "integer", "description": "Task ID to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "task_id": {"type": "integer", "description": "Task ID to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify task title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "task_id": {"type": "integer", "description": "Task ID to update"},
                            "title": {"type": "string", "description": "New task title (optional)"},
                            "description": {"type": "string", "description": "New task description (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]
        
        try:
            # Call OpenAI with tools
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # or gpt-3.5-turbo
                messages=conversation_history,
                tools=tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # Process tool calls if any
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # In a real implementation, this would call the MCP server
                    # For now, we'll simulate the tool call
                    result = await self.execute_tool_call(function_name, function_args)
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                
                # Get final response after tool execution
                if tool_results:
                    final_response = self.client.chat.completions.create(
                        model="gpt-4-turbo-preview",
                        messages=conversation_history + [response_message] + tool_results
                    )
                    final_content = final_response.choices[0].message.content
                else:
                    final_content = response_message.content
            else:
                final_content = response_message.content or "I processed your request."
            
            return {
                "response": final_content,
                "tool_calls": [
                    {
                        "name": tc.function.name,
                        "arguments": json.loads(tc.function.arguments)
                    } for tc in tool_calls
                ] if tool_calls else []
            }
        
        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "tool_calls": []
            }
    
    async def execute_tool_call(self, function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call (in a real implementation, this would connect to the MCP server)
        For now, we'll simulate the behavior
        """
        # In a real implementation, this would make an actual call to the MCP server
        # For simulation purposes, we'll return mock responses
        
        if function_name == "add_task":
            # Simulate adding a task
            return {
                "task_id": 1,  # Simulated new task ID
                "status": "created",
                "title": function_args.get("title", "Untitled task")
            }
        elif function_name == "list_tasks":
            # Simulate listing tasks
            return [
                {"id": 1, "title": "Sample task", "completed": False},
                {"id": 2, "title": "Another task", "completed": True}
            ]
        elif function_name == "complete_task":
            # Simulate completing a task
            return {
                "task_id": function_args.get("task_id"),
                "status": "completed",
                "title": "Sample completed task"
            }
        elif function_name == "delete_task":
            # Simulate deleting a task
            return {
                "task_id": function_args.get("task_id"),
                "status": "deleted",
                "title": "Sample deleted task"
            }
        elif function_name == "update_task":
            # Simulate updating a task
            return {
                "task_id": function_args.get("task_id"),
                "status": "updated",
                "title": function_args.get("title", "Updated task")
            }
        else:
            return {"error": f"Unknown function: {function_name}"}