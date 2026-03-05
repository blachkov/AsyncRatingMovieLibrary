from data.database import insert_query, read_query, update_query
from data.models import Movie

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