from supabase import create_client, Client
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional

class DatabaseConfig(BaseModel):
    url: str
    key: str

class Database:
    def __init__(self, config: DatabaseConfig):
        self.supabase_url = config.url
        self.supabase_key = config.key
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    async def fetch(self, table: str, id: Optional[str] = None, filter: Optional[dict] = None):
        try:
            if id:
                data = await self.supabase.from_(table).select('*').eq('id', id)
            elif filter:
                data = await self.supabase.from_(table).select('*').eq(filter)
            else:
                data = await self.supabase.from_(table).select('*')
            return data.execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def insert(self, table: str, data: dict):
        try:
            result = await self.supabase.from_(table).insert([data])
            return result.execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update(self, table: str, id: str, data: dict):
        try:
            result = await self.supabase.from_(table).update([data]).eq('id', id)
            return result.execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete(self, table: str, id: str):
        try:
            result = await self.supabase.from_(table).delete().eq('id', id)
            return result.execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def get_database_config():
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        raise HTTPException(status_code=500, detail='Supabase URL and key are required')
    return DatabaseConfig(url=supabase_url, key=supabase_key)

def get_database():
    config = get_database_config()
    return Database(config)