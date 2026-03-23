from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Initialize Supabase client
supabase_url = SUPABASE_URL
supabase_key = SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT authentication
def authenticate_user(username: str, password: str):
    try:
        user = supabase.from_("users").select("*").eq("username", username).execute()
        if user.data:
            user_data = user.data[0]
            if user_data["password"] == password:
                return user_data
        raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        token_data = {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = supabase.from_("users").select("*").eq("username", token_data["username"]).execute()
    if user.data:
        return user.data[0]
    raise HTTPException(status_code=401, detail="Invalid token")

# Include routes
from routes import User, Todo

app.include_router(User.router)
app.include_router(Todo.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Todo App API"}

# Error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})