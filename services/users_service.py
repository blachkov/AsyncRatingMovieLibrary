from sqlite3 import IntegrityError
from common.responses import BadRequest
from data.database import insert_query, read_query, update_query
from data.models import User

_SEPARATOR = ';'

def create_token(user: User) -> str:
    # This can be replaced with JWT in future
    return f'{user.id}{_SEPARATOR}{user.username}'

def is_authenticated(token: str) -> bool:
    return any(read_query(
        'SELECT 1 FROM users where id = ? and username = ?',
        token.split(_SEPARATOR)))
    # note: this token is not particulary secure, use JWT for real-world user

def from_token(token: str) -> User | None:
    if token:
        _, username = token.split(_SEPARATOR)
        return find_by_username(username)
    
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