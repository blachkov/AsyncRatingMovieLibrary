from fastapi import APIRouter, Header, Response
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, Unauthorized
from data.models import User
from services import users_service

users_router = APIRouter(prefix='/users')