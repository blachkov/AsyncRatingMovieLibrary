from pydantic import BaseModel

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
    title: str
    director: str
    release_year: int
    rating: int

    @classmethod
    def from_query_result(cls, id, title, director, release_year, rating):
        return cls(
            id=id,
            title=title,
            director=director,
            release_year=release_year,
            rating=rating)
