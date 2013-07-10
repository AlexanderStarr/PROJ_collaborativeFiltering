'''
>>> userList = createUserList()
>>> movieList = createMovieList()
>>> userList[10]
{'gender': 'F', 'age': 39, 'zip': '30329', 'occupation': 'other'}
>>> userList[20]
{'gender': 'M', 'age': 26, 'zip': '30068', 'occupation': 'writer'}
>>> len(userList)
943
>>> movieList[100]
{'genre': [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 'IMDB url': 'http://us.imdb.com/M/title-exact?Heavy%20Metal%20(1981)', 'video release date': '', 'release date': '08-Mar-1981', 'title': 'Heavy Metal (1981)'}
>>> movieList[1000]
{'genre': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'IMDB url': 'http://us.imdb.com/M/title-exact?Stupids,%20The%20(1996)', 'video release date': '', 'release date': '30-Aug-1996', 'title': 'Stupids, The (1996)'}
>>> movieList[1500]
{'genre': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 'IMDB url': 'http://us.imdb.com/M/title-exact?Kavkazsky%20Plennik%20(1996)', 'video release date': '', 'release date': '31-Jan-1997', 'title': 'Prisoner of the Mountains (Kavkazsky Plennik) (1996)'}
>>> len(movieList)
1682
>>> [rLu, rLm] = createRatingsList(len(userList), len(movieList))
>>> sum([len(x) for x in rLu])
100000
>>> sum([len(x) for x in rLm])
100000
>>> len(rLu)
943
>>> len(rLm)
1682
>>> len(rLu[1])
62
>>> sorted(rLu[1].keys())
[1, 10, 13, 14, 19, 25, 50, 100, 111, 127, 237, 242, 251, 255, 257, 258, 269, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316]
>>> [2 in rLm[x-1] for x in rLu[1].keys()]
[True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
>>> sorted([x for x in rLu[1].keys() if rLu[1][x] == 5])
[50, 100, 127, 242, 251, 272, 275, 283, 285, 302, 311, 313, 316]
>>> genreList = createGenreList()
>>> genreList[2]
'Adventure'
>>> len(genreList)
19
>>> sorted([(meanUserRating(x, rLu), x) for x in range(1, len(userList)+1)], reverse = True)[:5]
[(4.869565217391305, 849), (4.833333333333333, 688), (4.724137931034483, 507), (4.703703703703703, 628), (4.6875, 928)]
>>> sorted(rLu[849].values(), reverse=True)
[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 2, 1, 1]
>>> len(rLu[849])
51
>>> sorted([(meanMovieRating(x, rLm), x) for x in range(1, len(movieList)+1)], reverse = True)[:5]
[(5.0, 1653), (5.0, 1599), (5.0, 1536), (5.0, 1500), (5.0, 1467)]
>>> movieList[1652]["title"]
'Entertaining Angels: The Dorothy Day Story (1996)'
>>> movieList[1598]["title"]
"Someone Else's America (1995)"
>>> movieList[1535]["title"]
'Aiqing wansui (1994)'
>>> movieList[1499]["title"]
'Santa with Muscles (1996)'
>>> movieList[1466]["title"]
'Saint of Fort Washington, The (1993)'
>>> sorted([(meanUserRating(x, rLu), x) for x in range(1, len(userList)+1) if len(rLm[x]) >= 50], reverse = True)[:5]
[(4.833333333333333, 688), (4.724137931034483, 507), (4.703703703703703, 628), (4.563380281690141, 686), (4.548387096774194, 427)]
>>> movieList[687]["title"]
'Leave It to Beaver (1997)'
>>> movieList[506]["title"]
'Streetcar Named Desire, A (1951)'
>>> movieList[627]["title"]
'Sleepers (1996)'
>>> movieList[685]["title"]
'Perfect World, A (1993)'
>>> sorted(moviesInGenre(2, movieList))[:10]
['20,000 Leagues Under the Sea (1954)', 'Abyss, The (1989)', 'Adventures of Pinocchio, The (1996)', 'Adventures of Robin Hood, The (1938)', 'African Queen, The (1951)', 'Akira (1988)', 'Alaska (1996)', 'Amazing Panda Adventure, The (1995)', 'Anaconda (1997)', 'Andre (1994)']
>>> genreList[2]
'Adventure'
>>> sorted(moviesInGenre(genreList.index('Sci-Fi'), movieList))[:5]
['20,000 Leagues Under the Sea (1954)', '2001: A Space Odyssey (1968)', 'Abyss, The (1989)', 'Akira (1988)', 'Alien (1979)']
>>> popularMoviesInGenre(genreList.index('Sci-Fi'), movieList, rLm)[:5]
[('Star Wars (1977)', 4.3584905660377355), ('Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (1963)', 4.252577319587629), ('Empire Strikes Back, The (1980)', 4.204359673024523), ('Blade Runner (1982)', 4.138181818181818), ('Alien (1979)', 4.034364261168385)]
>>> popularMoviesInGenre(genreList.index('Musical'), movieList, rLm)[:5]
[('Wizard of Oz, The (1939)', 4.0772357723577235), ('Top Hat (1935)', 4.0476190476190474), ("Singin' in the Rain (1952)", 3.9927007299270074), ('This Is Spinal Tap (1984)', 3.905759162303665), ('Blues Brothers, The (1980)', 3.8366533864541834)]
>>> sorted([meanGenreRating(x, movieList, rLm) for x in range(len(genreList))], reverse = True)[:5]
[3.9215233698788228, 3.815811874866993, 3.6873793708484772, 3.6728232189973613, 3.63813155386082]
>>> popularGenres(genreList, movieList, rLm)
['Film-Noir', 'War', 'Drama', 'Documentary', 'Mystery', 'Crime', 'Romance', 'Western', 'Animation', 'Sci-Fi', 'Musical', 'Thriller', 'Adventure', 'Action', 'Comedy', "Children's", 'Horror', 'Fantasy', 'unknown']
'''
#-------------------------------------------------------
from project2 import *
#-------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod()
