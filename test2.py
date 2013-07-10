'''
>>> userList = createUserList()
>>> movieList = createMovieList()
>>> numUsers = len(userList)
>>> numMovies = len(movieList)
>>> [rLu, rLm] = createRatingsList(numUsers, numMovies)
>>> friends = kNearestNeighbors(1, rLu, 10)
>>> sorted([(x[0], round(x[1], 3)) for x in friends])
[(1, 1.0), (155, 1.0), (166, 0.981), (341, 1.0), (351, 0.996), (418, 1.0), (685, 1.0), (810, 0.901), (811, 0.988), (812, 1.0)]
>>> predictedRating(1, 1, rLu, friends)
5
>>> predictedRating(1, 2, rLu, friends)
3
>>> round(predictedRating(1, 273, rLu, friends), 3)
3.61
>>> round(max([predictedRating(1, i, rLu, friends) for i in range(1, numMovies+1)]), 3)
5.974
>>> friends = kNearestNeighbors(1, rLu, 100)
>>> round(predictedRating(1, 273, rLu, friends), 3)
3.506
>>> round(max([predictedRating(1, i, rLu, friends) for i in range(1, numMovies+1)]), 3)
5.61
>>> friends = [(418, 1.0)]
>>> round(meanUserRating(1, rLu), 3)
3.61
>>> ratings = [(predictedRating(1, i, rLu, friends), i) for i in range(270, 291)]
>>> [(round(x[0], 3), x[1]) for x in ratings]
[(5.0, 270), (2.0, 271), (3.0, 272), (3.61, 273), (3.61, 274), (3.61, 275), (3.61, 276), (3.61, 277), (3.61, 278), (3.61, 279), (3.61, 280), (3.61, 281), (3.61, 282), (3.61, 283), (3.61, 284), (3.61, 285), (3.61, 286), (3.61, 287), (5.71, 288), (3.61, 289), (3.61, 290)]
>>> friends = [(418, 1.0), (1, 1.0)]
>>> ratings = [(predictedRating(1, i, rLu, friends), i) for i in range(270, 291)]
>>> [(round(x[0], 3), x[1]) for x in ratings]
[(5.0, 270), (2.0, 271), (3.0, 272), (3.61, 273), (3.61, 274), (3.61, 275), (3.61, 276), (3.61, 277), (3.61, 278), (3.61, 279), (3.61, 280), (3.61, 281), (3.61, 282), (3.61, 283), (3.61, 284), (3.61, 285), (3.61, 286), (3.61, 287), (5.71, 288), (3.61, 289), (3.61, 290)]
>>> friends = [(418, 1.0), (1, 1.0), (2, -1)]
>>> ratings = [(predictedRating(1, i, rLu, friends), i) for i in range(270, 281)]
>>> [(round(x[0], 3), x[1]) for x in ratings]
[(5.0, 270), (2.0, 271), (3.0, 272), (3.901, 273), (2.901, 274), (4.901, 275), (3.901, 276), (3.901, 277), (2.901, 278), (3.901, 279), (2.901, 280)]
>>> friends = kNearestNeighbors(1, rLu, 100)
>>> topMovies = topKMovies(1, rLu, numMovies, 5, friends)
>>> sorted([(x[0], round(x[1], 3)) for x in topMovies])
[(923, 5.357), (1006, 5.61), (1084, 5.375), (1177, 5.313), (1388, 5.61)]
>>> sorted([movieList[x[0]-1]["title"] for x in topMovies])
['Anne Frank Remembered (1995)', 'Dunston Checks In (1996)', 'Gabbeh (1996)', 'Raise the Red Lantern (1991)', 'Until the End of the World (Bis ans Ende der Welt) (1991)']
>>> friends = kNearestNeighbors(2, rLu, 100)
>>> topMovies = topKMovies(2, rLu, numMovies, 9, friends)
>>> sorted([(x[0], round(x[1], 3)) for x in topMovies])
[(106, 5.362), (320, 5.421), (571, 6.875), (889, 5.671), (922, 5.568), (1053, 5.383), (1063, 6.875), (1554, 5.875), (1629, 5.362)]
>>> sorted([movieList[x[0]-1]["title"] for x in topMovies])
['Another Stakeout (1993)', 'Dead Man (1995)', 'Diabolique (1996)', 'Little Princess, A (1995)', 'Nico Icon (1995)', 'Now and Then (1995)', 'Paradise Lost: The Child Murders at Robin Hood Hills (1996)', 'Safe Passage (1994)', 'Tango Lesson, The (1997)']
>>> [predictedRating(500, 50, rLu, kNearestNeighbors(500, rLu, i)) for i in range(20, 31)]
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
'''
#-------------------------------------------------------
from project2 import *
#-------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod()
