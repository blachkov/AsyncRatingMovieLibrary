from fastapi import APIRouter, Response, Header
from common.responses import BadRequest, NoContent, NotFound, Unauthorized
from data.models import Movie
from services import movies_service

movies_router = APIRouter(prefix='/movies')

@movies_router.get('/')
def get_movies(
    name: str | None = None,
    sort: str | None = None,
):
    result = movies_service.all(name,sort)
    return result