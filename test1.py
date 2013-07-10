'''
>>> userList = createUserList()
>>> movieList = createMovieList()
>>> numUsers = len(userList)
>>> numMovies = len(movieList)
>>> [rLu, rLm] = createRatingsList(numUsers, numMovies)
>>> [0.99 < similarity(i, i, rLu) < 1.01 for i in range(1, numUsers+1)].count(True) == numUsers
True
>>> [-1.01 < similarity(1, i, rLu) < 1.01 for i in range(1, numUsers+1)].count(True) == numUsers
True
>>> sim = sorted([(similarity(1, i, rLu), i) for i in range(2, numUsers+1)], reverse = True)[:5]
>>> sorted([x[1] for x in sim])
[155, 341, 418, 685, 812]
>>> commonMovies = [m for m in range(1, numMovies+1) if m in rLu[0] and m in rLu[417]]
>>> commonMovies
[258, 269]
>>> rLu[0][258]
5
>>> rLu[417][258]
5
>>> rLu[0][269]
5
>>> rLu[417][269]
5
>>> sim = sorted([(similarity(1, i, rLu), i) for i in range(2, numUsers+1)])[:4]
>>> sorted([x[1] for x in sim])
[88, 631, 688, 729]
>>> L = [(similarity(i, j, rLu), i, j) for i in range(1, 501) for j in range(1, 501)]
>>> [x[1:] for x in L if x[0] > 0.95 and x[1] < x[2] and len([y for y in rLu[x[1]-1].keys() if y in rLu[x[2]-1]]) > 6]
[(8, 433), (17, 449), (22, 199), (47, 385), (79, 120), (118, 476), (123, 333)]
>>> sorted([(round(x[1], 3), x[0]) for x in kNearestNeighbors(500, rLu, 10)], reverse = True)
[(1.0, 500), (0.81, 273), (0.805, 813), (0.791, 557), (0.785, 171), (0.742, 729), (0.715, 47), (0.709, 414), (0.697, 789), (0.679, 166)]
>>> sorted([(x[0], round(x[1], 3)) for x in kNearestNeighbors(200, rLu, 70) if x[0] != 200 and round(x[1], 3) == 1])
[(688, 1.0)]
'''
#-------------------------------------------------------
from project3 import *
#-------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod()
