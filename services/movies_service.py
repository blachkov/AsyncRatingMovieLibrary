import httpx

from data.database import insert_query, read_query, update_query
from data.models import Movie
_API = 'http://www.omdbapi.com/?t='
_KEY = '&apikey=c6a2d834'
def all(title: str = None,
        sort: str = None):
    
    sql = '''SELECT id, title, director, release_year, rating FROM movies'''
    conditions: list[str] = []
    params: list = []

    if title:
        conditions.append('title LIKE ?')
        params.append(f"%{title}%")

    if conditions:
        sql += ' WHERE ' + ' AND '.join(conditions)

    if sort and sort.lower() in ('asc', 'desc'):
        sql += f' ORDER BY rating {sort.upper()}'

    rows = read_query(sql, tuple(params))
    return [Movie.from_query_result(*row) for row in rows]

def get_by_id(id: int) -> Movie:
    data = read_query(
        '''SELECT id, title, director, release_year, rating
            FROM movies
            WHERE id = ?''', (id,))

    return next((Movie.from_query_result(*row) for row in data), None)

def movie_exists(movie_title: str):
    data = read_query(
            '''SELECT title
               FROM movies
               WHERE title LIKE ?''', (f'%{movie_title}%',))
    if data:
        return True
    else:
        return False
    
def create(movie: Movie) -> Movie:
    generated_id = insert_query(
        'INSERT INTO movies(title,director,release_year,rating) VALUES(?,?,?,?)',
        (movie.title, movie.director, movie.release_year, 0))
    movie.id = generated_id
    return Movie.from_query_result(movie.id, movie.title, movie.director, movie.release_year, 0)

def create_async(movie_rating,movie:Movie):
    merged = Movie(
        id=movie.id,
        director=movie.director,
        title=movie.title,
        release_year=movie.release_year,
        rating=movie_rating
    )
    update_query(
        '''UPDATE movies SET
            rating = ?
            WHERE id = ?
        ''',
        (movie_rating, movie.id))
    return Movie.from_query_result(merged.id, merged.director, merged.title, merged.release_year, merged.rating)

def delete(movie:Movie):
    update_query('DELETE FROM movies WHERE id = ?', (movie.id,))

async def fetch_and_update_metascore(movie: Movie, dummy: Movie):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{_API}{movie.title}{_KEY}')
        film = response.json()
        create_async(film["Metascore"], dummy)