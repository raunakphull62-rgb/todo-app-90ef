from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import User as SupabaseUser
from supabase.exceptions import ClientException
from jose import jwt
from datetime import datetime, timedelta
from typing import List
from schemas.User import User, UserCreate, UserUpdate
from auth import verify_token
from config import settings
from database import supabase_url, supabase_key

supabase: Client = create_client(supabase_url, supabase_key)

router = APIRouter()

class UserRouter:
    @staticmethod
    @router.post("/users/")
    async def create_user(user: UserCreate):
        try:
            data = user.dict()
            data['password'] = jwt.encode({'password': data['password']}, settings.jwt_secret, algorithm='HS256')
            new_user = await supabase.from_('users').insert([data])
            return new_user.data[0]
        except ClientException as e:
            raise HTTPException(status_code=400, detail=e.message)

    @staticmethod
    @router.get("/users/")
    async def read_users(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            user_id = verify_token(token.credentials)
            users = await supabase.from_('users').select('*')
            return users.data
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    @staticmethod
    @router.get("/users/{user_id}")
    async def read_user(user_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            user_id_from_token = verify_token(token.credentials)
            if user_id_from_token != user_id:
                raise HTTPException(status_code=401, detail='Unauthorized')
            user = await supabase.from_('users').select('*').eq('id', user_id)
            return user.data[0]
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    @router.put("/users/{user_id}")
    async def update_user(user_id: int, user: UserUpdate, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            user_id_from_token = verify_token(token.credentials)
            if user_id_from_token != user_id:
                raise HTTPException(status_code=401, detail='Unauthorized')
            data = user.dict(exclude_unset=True)
            updated_user = await supabase.from_('users').update([data]).eq('id', user_id)
            return updated_user.data[0]
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    @router.delete("/users/{user_id}")
    async def delete_user(user_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            user_id_from_token = verify_token(token.credentials)
            if user_id_from_token != user_id:
                raise HTTPException(status_code=401, detail='Unauthorized')
            await supabase.from_('users').delete().eq('id', user_id)
            return {'message': 'User deleted'}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))