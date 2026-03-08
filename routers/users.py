from fastapi import APIRouter, Header, Response
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, Unauthorized
from data.models import User, LoginRequest
from services import users_service

users_router = APIRouter(prefix='/users')

@users_router.post('/login')
def login(credentials: LoginRequest):
    user = users_service.find_by_username(credentials.username)
    
    if not user or user.password != credentials.password:
        return Unauthorized('Invalid username or password')
    
    token = users_service.create_token(user)
    return {'access_token': token, 'token_type': 'bearer', 'username': user.username, 'role': user.role}

