from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

class User(BaseModel):
    id: int | None=None
    username: str
    password: str
    role: str

    @classmethod
    def from_query_result(cls, id, username, password, role):
        return cls(
            id=id,
            username=username,
            password=password,
            role=role)
    
class Movie(BaseModel):
    id: int | None=None
    title: Annotated[str, StringConstraints(min_length=1)]
    director: Annotated[str, StringConstraints(min_length=1)]
    release_year: Annotated[int,Field(gt=1930,lt=2027)]
    rating: int | None = None

    @classmethod
    def from_query_result(cls, id, title, director, release_year, rating):
        return cls(
            id=id,
            title=title,
            director=director,
            release_year=release_year,
            rating=rating)
