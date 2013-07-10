# Alexander Starr
# 22C:016:A01
# 00567613

def createUserList():
    # Reads from the file u.user and returns a list containing all demographic
    # information pertaining to the users.
    
    user_list = []   # Initialize the list of users
    template = ["age", "gender", "occupation", "zip"]
    f = open("u.user", "r")
    line = f.readline().rstrip()
    while line:
        # As long as line is non-empty, this will run. First the line is split
        # into a list, with each element being a piece of demographic info,
        # and the first element dropped because it is unimportant.
        user_info = line.split("|")[1:]
        
        # Then the age (index 0) is converted to an integer.
        user_info[0] = int(user_info[0])
        
        # Then the dictionary for the user is created, using the template list
        # for keys and user_info for values.
        user_dict = dict(zip(template, user_info))
        
        # The user_dict is appended to user_list and the next line retrieved.
        user_list.append(user_dict)
        line = f.readline().rstrip()
    f.close()
    return user_list

def createMovieList():
    # Reads from the file u.item and returns a list containing all of the info
    # pertaining to movies in the file.
    
    movie_list = []     # Initializes the list of movies
    template = ["title", "release date", "video release date",
                "IMDB url", "genre"]
    f = open("u.item", "r")
    line = f.readline().rstrip()
    while line:
        # As long as line is non-empty, this will execute.
        # First the line is split into a list, each element being a piece
        # of info about the movie.  The first element is dropped.
        movie_info = line.split("|")[1:]
        
        # Then the genre list is built from movie_info.
        genres = map(int, movie_info[4:])
        
        # The multiple genre elements of movie_info are replace with one list
        movie_info[4:] = [genres]
        
        # Then the dictionary is built, using the template list for keys and
        # the movie_info list for values
        movie_dict = dict(zip(template, movie_info))
        
        # The movie_dict is appended to the movie_list and next line retrieved.
        movie_list.append(movie_dict)
        line = f.readline().rstrip()
    f.close()
    return movie_list

def createRatingsList(numUsers, numMovies):
    # Reads from the file u.data and returns two lists containing all 100,000
    # ratings provided in the file.  rLu contains one element per user, with
    # that element containing all ratings from that user.  Same with rLm, but
    # each element contains all ratings for that movie.
    
    # First rLu is initialized to a list full of empty dictionaries.
    rLu = []
    for i in range(numUsers):
        rLu.append({})
    
    # Then rLm is initialized the same way.    
    rLm = []
    for i in range(numMovies):
        rLm.append({})
        
    # Now the file is opened, each line read, and the data added to rLu and rLm.
    f = open("u.data", "r")
    line = f.readline().rstrip()
    while line:
        # After the line is stripped, it is split by the tab character \t.
        # The split line has data like so: [userID, itemID, rating, timestamp]
        # For better readability, these are given their own variable, instead
        # of being elements in a list. They are also converted to integers.
        userID, itemID, rating, time = map(int, line.split("\t"))
        
        # The rating is then stored under both the user and the item lists
        # in the appropriate dictionary.
        rLu[userID - 1][itemID] = rating
        rLm[itemID - 1][userID] = rating
        line = f.readline().rstrip()
    f.close()
    return rLu, rLm

def createGenreList():
    # Reads from the file u.genre and returns a list of genres in order.
    genre_list = []   # Initializes the genre list.
    f = open("u.genre", "r")
    line = f.readline().rstrip()
    while line:
        # For every line, the line is split into a list, with element 0 being
        # the genre.  This is then appended to the genre_list.
        genre = line.split("|")[0]
        genre_list.append(genre)
        line = f.readline().rstrip()
    return genre_list

# returns the mean rating provided by user with id u. The second argument is 
# the ratings list containing ratings per user. 
def meanUserRating(u, userRatings):
    ratings = userRatings[u - 1].values()
    return getMean(ratings)
    
# returns the mean rating received by a movie with id u. The second argument is
# the ratings list containing ratings per movie. 
def meanMovieRating(u, movieRatings):
    ratings = movieRatings[u - 1].values()
    return getMean(ratings)

# Given a genre ID and a movie list, this function returns the list of all movie
# titles in the given genre, sorted in alphabetical order. 
def moviesInGenre(genre, movieList):
    movie_titles = []
    for movie in movieList:
        # movie["genre"] is a list, and movie["genre"][genre] is either 1 
        # (if the movie is in that genre) or 0 (movie not in genre).
        in_genre = movie["genre"][genre]
        if in_genre:
            movie_titles.append(movie["title"])
    movie_titles.sort()
    return movie_titles

# This function takes a genre ID, movie list and the ratings list containing
# ratings per movies. It returns a list of tuples containing movie titles and
# associated mean ratings. This list should only contain movie titles of the
# given genre that have received at least 20 ratings and should be sorted in
# decreasing order of mean rating received.
def popularMoviesInGenre(genre, movieList, movieRatings):
    popular = []
    for i in range(len(movieList)):
        # Iterates through the movie list, checking if a movie is in the genre
        # and if it has enough ratings.  If so, it inserts it in the list.
        ratings_dict = movieRatings[i]
        in_genre = movieList[i]["genre"][genre]
        enough_ratings = (len(ratings_dict) >= 20)
        if in_genre and enough_ratings:
            title = movieList[i]["title"]
            mean = getMean(ratings_dict.values())
            # The popular list sorted as it is built, eliminating the
            # need to sort after building.  A modified version of binarySearch
            # is used to find which index to insert the (title, mean) tuple.
            index = binarySearch(popular, (title, mean))
            popular.insert(index, (title, mean))
    return popular

# This function takes a genre ID, movie list and the ratings list containing
# ratings per movies. It returns the mean rating for the given genre, which is
# the mean taken over all ratings of all movies in the genre. 
def meanGenreRating(genre, movieList, movieRatings):
    genre_ratings = []
    for i in range(len(movieList)):
        in_genre = movieList[i]["genre"][genre]
        if in_genre:
            genre_ratings.extend(movieRatings[i].values())
    mean = getMean(genre_ratings)
    return mean

# This function takes a genre list, movie list and the ratings list containing
# ratings per movies. It returns a sorted list of genres, sorted in decreasing
# order of mean rating. 
def popularGenres(genreList, movieList, movieRatings):
    # First we find the mean for each genre and store it as a tuple with the
    # format (mean, genre) in the list genre_ratings
    genre_ratings = []
    for i in range(len(genreList)):
        mean = meanGenreRating(i, movieList, movieRatings)
        genre = genreList[i]
        genre_ratings.append((mean, genre))
    
    # Then we sort genre_ratings.
    genre_ratings.sort()
    
    # Finally we return a list of the second element of each tuple in L,
    # counting backwards.
    return [x[1] for x in genre_ratings[::-1]]

def getMean(L):
    # Gets the mean as a float of a list L
    mean = float(sum(L))/float(len(L))
    return mean

def binarySearch(L, tup):
    # Borrowed from previous assignment and modified to search through a list
    # of tuples which are arranged in descending order of the second element.
    # Takes a list and a tuple as arguments, then returns the index at which
    # the tuple should be inserted.
    left = 0 
    right = len(L)-1
    
    if left > right:
        # Only occurs if L is an empty list.
        return 0
    
    while left <= right:
        # Iterates until either the value is found in the list, or the slice
        # being searched no longer contains multiple elements.
        mid = (left + right) / 2
        if L[mid][1] == tup[1]:
            return mid
        elif L[mid][1] > tup[1]:
            left = mid + 1
        elif L[mid][1] < tup[1]:
            right = mid - 1
            
    # If this is reached, then the value was not found, so we must determine
    # where to place the tuple relative to its closest neighbor.
    if L[mid][1] < tup[1]:
        return mid
    else:
        return mid +1

# The below lines were used for testing purposes.
'''rLu, rLm = createRatingsList(943, 1682)
userList = createUserList()
movieList = createMovieList()
genreList = createGenreList()'''
