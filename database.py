import os
import datetime
import psycopg2  # environment postgres conf

from dotenv import load_dotenv

load_dotenv()  # can take dot.env file

# Table that stores the movies and their releases
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

# Table that stores the username
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

# Table that stores the username
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """select movies.* 
from movies 
join watched on movies.id = watched.movie_id
join users on users.username = watched.user_username 
where users.username = %s;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s)"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = %s;"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE %s"
CREATE_RELEASE_INDEX = "CREATE UNIQUE INDEX IF NOT EXISTS idx_movies_release ON  movies(release_timestamp); "


connection = psycopg2.connect(os.environ["DATABASE_URL"])


def create_tables():                    # no return because it just creates the table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASE_INDEX)


def add_user(username):                 # no return because it just inserts data provided to the table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def add_movie(title, release_timestamp):  # no return because it just inserts data provided to the table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIE, (title, release_timestamp))


def get_movies(upcoming=False):         # .fetchall(): all the results are returned to the variable used in the call
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()     # datetime module, class, and today method,
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))  # with today's date in it and the seconds(REAL)
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def search_movies(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
            return cursor.fetchall()


def watch_movie(username, movie_id):    # no return because it just insert data provided to the table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username):       # .fetchall(): all the results are returned to the variable used in the call
    with connection:                    # fetchone():  would just return one row
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()
