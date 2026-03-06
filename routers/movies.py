import asyncio
import time

from fastapi import APIRouter, Response, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NoContent, NotFound, Unauthorized
from data.models import Movie
from services import movies_service, users_service


movies_router = APIRouter(prefix='/movies')

@movies_router.get('/')
def get_movies(
    name: str | None = None,
    sort: str | None = None,
):
    result = movies_service.all(name,sort)
    return result

@movies_router.get('/{id}')
def get_movie_by_id(id: int):
    result = movies_service.get_by_id(id)
    if not result:
        return NotFound()
    return result

@movies_router.post('/')
async def create_movie(movie: Movie, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not users_service.is_admin(user):
        return Unauthorized('You cannot post movies')
    if movies_service.movie_exists(movie.title):
        return BadRequest(f'already exists')
    dummy = movies_service.create(movie)  # Returns immediately with rating=0
    asyncio.create_task(movies_service.fetch_and_update_metascore(movie, dummy))  # Fire and forget
    return dummy

@movies_router.delete('/{id}')
def delete_movie(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    movie = movies_service.get_by_id(id)
    if not users_service.is_admin(user):
        return Unauthorized('You cannot delete movies')
    if not movie:
        return BadRequest(f'No such movie')
    movies_service.delete(movie)
    return f"Movie {movie.title} has been deleted!"

@movies_router.put('/{id}')
def update_movie(id: int, new_movie: Movie, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    movie = movies_service.get_by_id(id)
    if not users_service.is_admin(user):
        return Unauthorized('You cannot edit movies')
    if not movie:
        return BadRequest(f'No such movie')
    result = movies_service.update(movie,new_movie)
    return result