from fastapi import APIRouter, Response, Header
from common.responses import BadRequest, NoContent, NotFound, Unauthorized
from data.models import Movie
from services import movies_service

movies_router = APIRouter(prefix='/movies')