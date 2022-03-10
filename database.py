import datetime
import sqlite3

# Table that stores the movies and their releases
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

# Table that stores the user name
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

# Table that stores the user name
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
INSERT_USER = "INSERT INTO users (username) VALUES (?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = """select movies.* 
from movies 
join watched on movies.id = watched.movie_id
join users on users.username = watched.user_username 
where users.username = ?;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (?, ?)"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE ?"


connection = sqlite3.connect("data.db")

def create_tables():                    # no return because it just creates the table
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE) 

def add_user(username):                 # no return because it just insert data provided to the table
    with connection:
        connection.execute(INSERT_USER, (username,))

def add_movie(title,release_timestamp): # no return because it just insert data provided to the table
    with connection:
        connection.execute(INSERT_MOVIE, (title,release_timestamp))

def get_movies(upcoming=False):         # .fetchall(): all the results are returned to the variable used in the call
    with connection:
        cursor = connection.cursor()    # takes the list
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp() # datetime module, class, and today method, with today's date in it and the seconds(REAL)
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()

def search_movies(search_term):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
        return cursor.fetchall()

def watch_movie(username, movie_id):    # no return because it just insert data provided to the table
    with connection:        
        connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))

def get_watched_movies(username):       # .fetchall(): all the results are returned to the variable used in the call
    with connection:                    # fetchone():  would just return one row
        cursor = connection.cursor()    # takes the list
        cursor.execute(SELECT_WATCHED_MOVIES, (username,) )
        return cursor.fetchall() 
