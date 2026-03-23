from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import SupabaseError
from datetime import datetime
from typing import List, Optional
from auth import authenticate_user
from config import SUPABASE_URL, SUPABASE_KEY
from schemas.Todo import Todo, TodoCreate, TodoUpdate

supabase_url: str = os.getenv("SUPABASE_URL", SUPABASE_URL)
supabase_key: str = os.getenv("SUPABASE_KEY", SUPABASE_KEY)
supabase: Client = create_client(supabase_url, supabase_key)

todo_router = APIRouter()
security = HTTPBearer()

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[datetime]
    user_id: int

@todo_router.get("/todos", response_model=List[TodoResponse])
async def get_all_todos(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = authenticate_user(token.credentials)
        data = supabase.from_("todos").select("*").eq("user_id", user.id).execute()
        return data.data
    except SupabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@todo_router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = authenticate_user(token.credentials)
        data = supabase.from_("todos").select("*").eq("id", todo_id).eq("user_id", user.id).execute()
        if not data.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return data.data[0]
    except SupabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@todo_router.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = authenticate_user(token.credentials)
        data = supabase.from_("todos").insert([todo.dict() | {"user_id": user.id}]).execute()
        return data.data[0]
    except SupabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@todo_router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo: TodoUpdate, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = authenticate_user(token.credentials)
        data = supabase.from_("todos").select("*").eq("id", todo_id).eq("user_id", user.id).execute()
        if not data.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        updated_data = supabase.from_("todos").update([todo.dict()]).eq("id", todo_id).eq("user_id", user.id).execute()
        return updated_data.data[0]
    except SupabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@todo_router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = authenticate_user(token.credentials)
        data = supabase.from_("todos").select("*").eq("id", todo_id).eq("user_id", user.id).execute()
        if not data.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        supabase.from_("todos").delete().eq("id", todo_id).eq("user_id", user.id).execute()
        return {"message": "Todo deleted successfully"}
    except SupabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))