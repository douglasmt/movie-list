import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Exit.

Your selection: """ #menu displayed when we need the user input
welcome = "Welcome to the watchlist app!" # Welcome message that is the first message to the user


print(welcome)
database.create_tables() #just the creation of the tables if they exist

def prompt_add_movie():                                         # for option 1 When the user chooses to register a movie
    title = input("Movie title: ")                                      # receives a movie title 
    release_date = input("Release date(dd-mm-YYYY): ")                  # receive an input in a data desired format
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")  # parse date : 2012-09-12 00:00:00
    timestamp = parsed_date.timestamp()                                 # Number of seconds since 1970 - timestamp:   1347418800.0
    database.add_movie(title, timestamp)

def print_movie_list(heading, movies):                          # for option 2 and 3
    print(f"-- {heading} movies --")                            # receives "Upcoming" if get_movies(True) or "All" if get_movies(EMPTY), and the movies 
    for movie in movies:                                        # takes the list in movies
        movie_date = datetime.datetime.fromtimestamp(movie[1])  # converts from timestamp:  1347418800.0
        human_date = movie_date.strftime("%d %b %Y")            # three letter month:       12 Jan 2023
        print(f"{movie[0]} (on {human_date})")                  # prints like:              Robin (on 12 Jan 2023)
    print("---- \n")

def print_watched_movie_list(username, movies):                 # for option 5, takes the name as condition
    print(f"-- {username} watched movies -- ")                  # presents the header for the user movies
    for movie in movies:                                        # movies listed in watched table by the user(watcher name)
        print(f"{movie[1]} ")                                   # shows the second parameter, movie title
    print("---- \n")



def prompt_watch_movie():                                       # for option 4 when the user register the watched movie
    username = input("Username: ")
    movie_title = input("Enter movie title you've watched: ")      
    database.watch_movie(username, movie_title)                 # function to delete in movies table and insert in watched table



while (user_input := input(menu)) != "6":                       # 6) Exit.
    if user_input == "1":                                       # 1) Add new movie.
        prompt_add_movie() 
    elif user_input == "2":                                     # 2) View upcoming movies.
        movies = database.get_movies(True)
        print_movie_list("Upcoming", movies)
    elif user_input == "3":                                     # 3) View all movies
        movies = database.get_movies()
        print_movie_list("All" , movies)
    elif user_input == "4":                                     # 4) Watch a movie
        prompt_watch_movie()
    elif user_input == "5":                                     # 5) View watched movies.
        username = input("Username: ")
        movies = database.get_watched_movies(username)
        print_watched_movie_list("Watched" , movies)
    else:
        print("Invalid input, please try again!")