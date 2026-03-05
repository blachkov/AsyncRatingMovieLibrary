from sqlite3 import connect

_DB_FILE = './data/dbfile.db'


def read_query(sql: str, sql_params=()):
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()
        
        return cursor.rowcount > 0

def query_count(sql: str, sql_params=()):
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return cursor.fetchone()[0]


def init_database():
    # Create tables
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        director TEXT,
                        release_year INTEGER,
                        rating REAL
                        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL
                        );''')
        
    if query_count('SELECT COUNT(*) from movies') == 0:
        print('Inserting movies')
        insert_query('''INSERT INTO movies(title,director,release_year) VALUES
                            ('Titanic','James Cameron','1997'),
                            ('Troy','Wolfgang Petersen','2004'),
                            ('Gladiator','Ridley Scott','2000')''')
        

    if query_count('SELECT COUNT(*) from users') == 0:
        print('Inserting users')
        insert_query('''INSERT INTO users(username,password,role) VALUES
                            ('Pesho','1234','user'),
                            ('Gosho','1234','admin'),
                            ('Tosho','1234','user')''')
        
        