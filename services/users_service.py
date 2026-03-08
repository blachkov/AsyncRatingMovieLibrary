from sqlite3 import IntegrityError
from datetime import datetime, timedelta, timezone
from jwt import encode, decode, InvalidTokenError
from common.responses import BadRequest
from data.database import insert_query, read_query, update_query
from data.models import User

_SECRET_KEY = 'your-secret-key-change-this-in-production'
_ALGORITHM = 'HS256'
_TOKEN_EXPIRATION_HOURS = 24

def create_token(user: User) -> str:
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.now(timezone.utc) + timedelta(hours=_TOKEN_EXPIRATION_HOURS)
    }
    return encode(payload, _SECRET_KEY, algorithm=_ALGORITHM)

def is_authenticated(token: str) -> bool:
    try:
        decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
        return True
    except InvalidTokenError:
        return False

def from_token(token: str) -> User | None:
    if not token:
        return None
    try:
        payload = decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
        username = payload.get('username')
        return find_by_username(username)
    except InvalidTokenError:
        return None
    
def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT id, username, password, role FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)

def is_admin(user: User):
    if user.role=="admin":
        return True
    else:
        return False