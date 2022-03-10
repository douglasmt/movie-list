import datetime
import sqlite3

# title, release_date, watched
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    title TEXT,
    release_timestamp REAL
);"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    watcher_name TEXT,
    title TEXT
)"""

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = ?;"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (watcher_name, title) VALUES (?, ?)"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"


connection = sqlite3.connect("data.db")

def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_WATCHLIST_TABLE)

def add_movie(title,release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIE, (title,release_timestamp))

def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp() # datetime module, class, and today method, with today's date in it and the seconds(REAL)
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def watch_movie(username, title):
    with connection:
        connection.execute(DELETE_MOVIE, (title,))
        connection.execute(INSERT_WATCHED_MOVIE, (username,title))

def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,) )
        return cursor.fetchall()