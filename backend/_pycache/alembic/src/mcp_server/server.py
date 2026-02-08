import asyncio
from typing import Dict, Any, List
from mcp import server
from mcp.server import MCPServer
from mcp.protocol import (
    InitializeRequest,
    ToolsListResult,
    Tool,
    CallToolRequest,
    SendConfigurationRequest,
    GetPromptRequest,
    Prompt,
    SendTelemetryRequest,
)
from sqlmodel import Session, select
from ..database import get_session
from ..tasks.models import Task, TaskCreate, TaskUpdate
from ..chatbot.conversation_models import Conversation, Message
from datetime import datetime


class TodoMCPServer:
    def __init__(self):
        self.server = MCPServer()
        self._setup_routes()
    
    def _setup_routes(self):
        @self.server.on_initialize
        async def initialize(request: InitializeRequest) -> Dict[str, Any]:
            return {
                "server_info": {
                    "name": "Todo AI Chatbot MCP Server",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {},
                    "prompts": {},
                    "configuration": {}
                }
            }
        
        @self.server.list_tools
        async def list_tools() -> ToolsListResult:
            tools = [
                Tool(
                    name="add_task",
                    description="Create a new task",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description (optional)"}
                        },
                        "required": ["user_id", "title"]
                    }
                ),
                Tool(
                    name="list_tasks",
                    description="Retrieve tasks from the list",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "status": {"type": "string", "description": "Filter by status: all, pending, completed (optional)"}
                        },
                        "required": ["user_id"]
                    }
                ),
                Tool(
                    name="complete_task",
                    description="Mark a task as complete",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "task_id": {"type": "integer", "description": "Task ID to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                ),
                Tool(
                    name="delete_task",
                    description="Remove a task from the list",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "task_id": {"type": "integer", "description": "Task ID to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                ),
                Tool(
                    name="update_task",
                    description="Modify task title or description",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User identifier"},
                            "task_id": {"type": "integer", "description": "Task ID to update"},
                            "title": {"type": "string", "description": "New task title (optional)"},
                            "description": {"type": "string", "description": "New task description (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                )
            ]
            return ToolsListResult(tools=tools)
        
        @self.server.call_tool
        async def call_tool(request: CallToolRequest) -> Any:
            tool_name = request.name
            arguments = request.arguments
            
            # Create a new session for each tool call
            session_gen = get_session()
            session = next(session_gen)
            
            try:
                if tool_name == "add_task":
                    return await self.add_task(session, arguments)
                elif tool_name == "list_tasks":
                    return await self.list_tasks(session, arguments)
                elif tool_name == "complete_task":
                    return await self.complete_task(session, arguments)
                elif tool_name == "delete_task":
                    return await self.delete_task(session, arguments)
                elif tool_name == "update_task":
                    return await self.update_task(session, arguments)
                else:
                    return {"error": f"Unknown tool: {tool_name}"}
            finally:
                session.close()
    
    async def add_task(self, session: Session, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Create Task object directly since TaskCreate doesn't include user_id
            db_task = Task(
                user_id=args["user_id"],
                title=args["title"],
                description=args.get("description"),
                completed=False
            )
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return {
                "task_id": db_task.id,
                "status": "created",
                "title": db_task.title
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def list_tasks(self, session: Session, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            user_id = args["user_id"]
            status = args.get("status", "all")  # Default to "all"
            
            query = select(Task).where(Task.user_id == user_id)
            
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            
            tasks = session.exec(query).all()
            
            return [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
                for task in tasks
            ]
        except Exception as e:
            return [{"error": str(e)}]
    
    async def complete_task(self, session: Session, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            task_id = args["task_id"]
            user_id = args["user_id"]
            
            task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
            
            if not task:
                return {"error": "Task not found"}
            
            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def delete_task(self, session: Session, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            task_id = args["task_id"]
            user_id = args["user_id"]
            
            task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
            
            if not task:
                return {"error": "Task not found"}
            
            session.delete(task)
            session.commit()
            
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": task.title
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def update_task(self, session: Session, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            task_id = args["task_id"]
            user_id = args["user_id"]
            
            task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
            
            if not task:
                return {"error": "Task not found"}
            
            # Update fields if provided
            if "title" in args and args["title"] is not None:
                task.title = args["title"]
            if "description" in args and args["description"] is not None:
                task.description = args["description"]
            
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def serve(self, host: str = "localhost", port: int = 3000):
        await self.server.start(host=host, port=port)


