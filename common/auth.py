from fastapi import HTTPException, Request
from data.models import User
from services.users_service import is_authenticated, from_token


def get_user_or_raise_401(token: str) -> User:
    if not is_authenticated(token):
        raise HTTPException(status_code=401)

    return from_token(token)

def get_user_if_token(request: Request):
    token = request.cookies.get('token')
    return from_token(token)