# Alexander Starr
# 22C:016:A01
# 00567613

import time
from math import sqrt
from random import randint

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

# Given the IDs of two users, u and v, and ratings list containing a ratings-
# dictionary per user, this function computes the similarity in ratings between
# the two users, using movies that the two users have commonly rated.
def similarity(u, v, userRatings):
    # First we calculate the values needed for the summations in the similarity
    # calculation, namely each user's mean and the movies common to both users.
    common_movies = commonElements(userRatings[u-1], userRatings[v-1])
    if not common_movies:
        # If u and v have no movies in common, then we assume they have sim 0
        return 0.0
    uMean = meanUserRating(u, userRatings)
    vMean = meanUserRating(v, userRatings)
    uStdDevSum = 0.0
    vStdDevSum = 0.0
    similaritySum = 0.0
    for m in common_movies:
        # For each movie ID in the common_movie list, we have three summations
        # to increment: the running total for the standard deviation of users u
        # and v (u/vStdDevSum), and similaritySum.
        uRatingDiff = userRatings[u-1][m] - uMean
        vRatingDiff = userRatings[v-1][m] - vMean
        uStdDevSum = uStdDevSum + (uRatingDiff ** 2)
        vStdDevSum = vStdDevSum + (vRatingDiff ** 2)
        similaritySum = similaritySum + (uRatingDiff * vRatingDiff)
    if uStdDevSum == 0 or vStdDevSum == 0:
        return 0.0
    uStdDev = sqrt(uStdDevSum)
    vStdDev = sqrt(vStdDevSum)
    similarity = similaritySum / (uStdDev * vStdDev)
    return similarity

def commonElements(S1, S2):
    # Takes two data structures and returns a list of all elements common to
    # both.  Arguments can be dictionaries or lists.
    common = []
    if len(S1) <= len(S2):
        # We can iterate through only the smaller list to save some time.
        for item in S1:
            if item in S2:
                common.append(item)
    else:
        for item in S2:
            if item in S1:
                common.append(item)
    return common
        

# Returns the list of (user ID, similarity)-pairs for the k users who are most
# similar to user u. The returned list of tuples is in decreasing order of
# similarity. 
def kNearestNeighbors(u, userRatings, k):
    nearest = []
    for v in range(len(userRatings)):
        # As long as v is not the same user as u, we find the similarity
        # then use the binarySearch() function to insert the tuple in the
        # list nearest.  Once built, the k first elements are returned.
        sim = similarity(u, v, userRatings)
        index = binarySearch(nearest, (v, sim))
        nearest.insert(index, (v, sim))
    return nearest[:k]

# Predicts a rating by user u for movie m. If u has already rated m, then it
# simply uses that rating. Otherwise it uses the ratings of the list of friends
# (the 4th parameter) to come up with a rating by u of m. Here, as usual,
# userRatings is the list of movie ratings that contains one ratings-dictionary
# per user. Typically the argument corresponding to friends would have been
# computed by a call to the kNearestNeighbors function. 
def predictedRating(u, m, userRatings, friends):
    if m in userRatings[u-1]:
        return userRatings[u-1][m]
    else:
        weightedRatingSum = 0.0
        similaritySum = 0.0
        # For every user in the friends list, if they have rated movie m,
        # then we add the weighted rating to weightedRatingSum, and add their
        # similarity to u to similaritySum.
        for friend in friends:
            # friend is a tuple, index 0 is the ID, index 1 the similarity to u.
            if m in userRatings[friend[0]-1]:
                friendMean = meanUserRating(friend[0], userRatings)
                weightedRating = ((userRatings[friend[0]-1][m] - friendMean) *
                                  friend[1])
                weightedRatingSum = weightedRatingSum + weightedRating
                similaritySum = similaritySum + friend[1]
        # Once both sums are calculated, we can compute the predicted rating.
        # If either sum is zero, then we should return zero.
        uMean = meanUserRating(u, userRatings)
        if weightedRatingSum and similaritySum:
            # When both sums are non-zero, then we calculate predicted.
            predicted = uMean + (weightedRatingSum / similaritySum)
        else:
            # If either sum is equal to zero, then this likely means that there
            # were no users in the friends list that have rated movie m, and
            # the best prediction we can make is simply the user's mean rating.
            predicted = uMean
        return predicted

# Returns the k movies with highest predicted ratings by the given user u.
# The returned list is a list of (movie, rating)-tuples. The function uses
# the provided list of friends to compute the ratings. You should think of
# friends as something that would have been computed by the kNearestNeighbors
# function. In other words, friends is a list of (user ID, similarity) pairs.
def topKMovies(u, userRatings, numMovies, k, friends):
    top = []
    for m in range(1, numMovies+1):
        predicted = predictedRating(u, m, userRatings, friends)
        index = binarySearch(top, (m, predicted))
        top.insert(index, (m, predicted))
    return top[:k]

# This function reads from the file u.data and returns a trainingSet of
# ratings and a test set of ratings. The test set is obtained by randomly 
# selecting 20,000 ratings. The remaining 80,000 ratings are returned as 
# the training set. The test set is a list of size 20,000, each element 
# having the form (user, movie, rating). The training set has a similar 
# form, but it is a list of 80,000 elements. it is expected that the user 
# will call this function as [trainingSet, testSet] = partitionRatings() 
def partitionRatings():
    full = []   # First we initialize the full data list.
    f = open("u.data", "r")
    line = f.readline().rstrip()
    # Then we scan through the file and build the full data list.
    while line:
        user, movie, rating, time = map(int, line.split("\t"))
        full.append((user, movie, rating))
        line = f.readline().rstrip()
    f.close()
    # We will then iterate 20,000 times, each time picking a random index
    # in bounds of the training set, then popping it and appending it to
    # the test set.  This is faster than using random.sample() and then
    # removing each element of the test set from the training set.
    training = full[:]
    test = []
    for x in range(20000):
        i = randint(0, len(training)-1)
        test.append(training.pop(i))
    return training, test

# Takes the raw list of rating-triples and converts this into data 
# structures containing the ratings, one from the point of view of users 
# and one from the point of view of movies. In addition, the 
# function takes the number of users and movies as parameters. It is expected 
# that this function will be called with the trainingSet constructed from a 
# call to partitionRatings(). This function no longer reads directly from the 
# file u.data. 
def createTrainingRatingsList(rawRatings, numUsers, numItems):
    # First rLu is initialized to a list full of empty dictionaries.
    rLu = []
    for i in range(numUsers):
        rLu.append({})
    
    # Then rLm is initialized the same way.    
    rLm = []
    for i in range(numItems):
        rLm.append({})
        
    # Then it will iterate through the rawRatings list, adding each rating
    # to the appropriate user and movie dictionaries.
    for item in rawRatings:
        # item[0] is the user ID, item[1] the movie ID, item[2] the rating.
        rLu[item[0] - 1][item[1]] = item[2]
        rLm[item[1] - 1][item[0]] = item[2]
    return rLu, rLm

# This function takes a test set of ratings and the ratings list that was 
# built from the training set and returns precision and recall. This function
# will be called as [precision, recall] = evaluateCF(testSet, rLu) 
def evaluateCF(testSet, rLu):
    # To find precision, we want to look for every movie with a predicted rating
    # >=4, and of those, count how many have an actual rating over 3.5.
    # To find recall, we want to look for every movie with an actual rating
    # >= 4, and of those, count how many have a predicted rating over 3.5.
    # So, we will go through every element in the testSet partition, and find
    # the predicted rating for that user/movie pair using only the training
    # set data.  Predicted/actual ratings over 3.5/4 will increment the proper
    # counter.  At the end, precision and recall are computed.
    actual_over_threefive = 0
    actual_over_four = 0
    predicted_over_threefive = 0
    predicted_over_four = 0
    # To make the runtime manageable, we will build a neighbor dictionary to
    # reference, so we don't have to compute friend lists for every rating, but
    # instead for every user.  Then we can reference this dictionary to pass
    # the friend list to predictedRating().
    neighborDict = buildNeighborsDict(rLu, 75)
    for item in testSet:
        user = item[0]
        movie = item[1]
        actual_rating = item[2]
        predicted_rating = predictedRating(user, movie, rLu, 
                                           neighborDict[user])
        if actual_rating >= 4:
            actual_over_four = actual_over_four + 1
            if predicted_rating >= 3.5: 
                predicted_over_threefive = predicted_over_threefive + 1
        if predicted_rating >= 4:
            predicted_over_four = predicted_over_four + 1
            if actual_rating >= 3.5:
                actual_over_threefive = actual_over_threefive + 1
    precision = float(actual_over_threefive) / float(predicted_over_four)
    recall = float(predicted_over_threefive) / float(actual_over_four)
    return precision, recall

def naivePrecisionRecall(testSet, rLu, rLm, algorithm):
    actual_over_threefive = 0
    actual_over_four = 0
    predicted_over_threefive = 0
    predicted_over_four = 0    
    for item in testSet:
        user = item[0]
        movie = item[1]
        actual_rating = item[2]
        if algorithm == "rand":
            predicted_rating = randPredictedRating()
        elif algorithm == "avg":
            predicted_rating = meanMovieRating(movie, rLm)
        if actual_rating >= 4:
            actual_over_four = actual_over_four + 1
            if predicted_rating >= 3.5: 
                predicted_over_threefive = predicted_over_threefive + 1
        if predicted_rating >= 4:
            predicted_over_four = predicted_over_four + 1
            if actual_rating >= 3.5:
                actual_over_threefive = actual_over_threefive + 1
    precision = float(actual_over_threefive) / float(predicted_over_four)
    recall = float(predicted_over_threefive) / float(actual_over_four)
    return precision, recall    

# Creates a dictionary which has user IDs as the keys, and a neighbors list
# corresponding to that user as the value.  Each neighbors list contains
# n users, and has the (userID, similarity) structure for each element.
def buildNeighborsDict(userRatings, n):
    neighborsDict = {}
    for userID in range(1, 944):
        neighborsDict[userID] = kNearestNeighbors(userID, userRatings, n)
    return neighborsDict

# The naive, random movie rating algorithm.
def randPredictedRating():
    return randint(1, 5)

# This runs the entire program, and will perform several computations of
# precision and recall using all three algoritms.
def mainProgram():
    # First we generate the data structures that don't change, and will
    # be used by other functions.
    rLu, rLm = createRatingsList(943, 1682)
    userList = createUserList()
    movieList = createMovieList()
    genreList = createGenreList()
    
    # Here is where we need to iterate. For each algorithm, we have a tuple
    # containing: a string of the name, a list for the precision values, and a
    # list for the recall values.  We will come up with 10 random train/test
    # partitions, and evaluate each algorithm for each partition.
    prCF = ("collaborative filtering", [], [])
    prRand = ("random rating", [], [])
    prAvg = ("average movie rating", [], [])
    for x in range(10):
        training, test = partitionRatings()
        trainrLu, trainrLm = createTrainingRatingsList(training, 943, 1682)
        pr = evaluateCF(test, trainrLu)
        prCF[1].append(pr[0])
        prCF[2].append(pr[1])
        pr = naivePrecisionRecall(test, trainrLu, rLm, "rand")
        prRand[1].append(pr[0])
        prRand[2].append(pr[1])
        pr = naivePrecisionRecall(test, trainrLu, rLm, "avg")
        prAvg[1].append(pr[0])
        prAvg[2].append(pr[1])      
    
    # Now we will build a dictionary to contain the average precision and recall
    # values for each algorithm, CF, Rand, and Avg.
    avgPrecisionRecall = []
    for T in [prCF, prRand, prAvg]:
        pAvg = float(sum(T[1])) / len(T[1])
        rAvg = float(sum(T[2])) / len(T[2])
        avgPrecisionRecall.append({"name": T[0], "precision": pAvg,
                                    "recall": rAvg})
    
    # All that is left is to display the data.  We can do this with some simple
    # looping and string concatenation.
    for item in avgPrecisionRecall:
        print "Values for " + item["name"] + " algorithm:"
        print "Precision: " + str(round(item["precision"], 3))
        print "Recall: " + str(round(item["recall"], 3)) + "\n"