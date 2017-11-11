import pandas as pd
import math
import random as rnd
import json
import requests

# quantity of users
square = 40
# my variant in task
userNumber = 24


# cos metric for data.csv
def sim(x, y):
    sum = 0
    sumSqrtX = 0
    sumSqrtY = 0
    for i in range(1, 31):
        if data[i][x] != -1 and data[i][y] != -1:
            sum += data[i][x] * data[i][y]
            sumSqrtX += pow(data[i][x], 2)
            sumSqrtY += pow(data[i][y], 2)

    return round((sum / (math.sqrt(sumSqrtX) * math.sqrt(sumSqrtY))), 3)


# calculate the average value for each user
def average_func():
    averageArray = []
    for j in range(0, 40):
        average = 0
        films = 0
        for i in range(1, 31):
            if data[i][j] != -1:
                average += data[i][j]
                films += 1
        averageArray.append(round((average / films), 3))
    return averageArray

# the result of this function we use in the case if there is no film to recommend
def max_movie(user):
    flagFound = False
    for y in range(1,31):
        if data[y][user] == 5 and flagFound is False:
            max_found_film = y
            flagFound = True
    return max_found_film


# read files
data = pd.read_csv("data.csv", sep=",", skiprows=[0], header=None)
context = pd.read_csv("context.csv", sep=",", skiprows=[0], header=None)

# FIRST PART OF HOMEWORK: TO CALCULATE RATING FOR NOT RATED FILMS

usersAverage = average_func()

# calculate sim for only my user
# user 1 : {user 1: .., user 2:.., user 3:.. ...}
metric = {}
for jy in range(square):
    if jy != userNumber - 1:
        metric.update({(jy + 1): sim(userNumber - 1, jy)})

# sort the data to get the list of sim from high to low
sortedDict = sorted(metric.items(), key=lambda x: x[1], reverse=True)

# get five appropriate users
user = []
additionalMovies = []
for x in range(5):
    user.append(sortedDict[x][0])
    additionalMovies.append(max_movie(sortedDict[x][0] - 1))
# list of final movies
movies = {}

filmsList = []
for x in range(1,31):
    if data[x][userNumber-1] == -1:
        filmsList.append(x)

# final rating
# denominator is lower part of fraction in formula
# nominator is higher part of fraction in formula
ri = 0
for i in filmsList:

    nominator = 0
    denominator = 0
    ri = 0
    for x in user:
        if data[i][x-1] != -1:
            nominator += sortedDict[x][1] * (data[i][x-1] - usersAverage[x-1])
            denominator += abs(sortedDict[x][1])
    ri = round((usersAverage[userNumber - 1] + nominator / denominator),3)
    movies.update({i:round(ri,3)})

# sort the data to get the list of sim from high rating to low
rangeMovies = sorted(movies.items(), key=lambda x: x[1], reverse=True)

# SECOND PART OF HOMEWORK: WHICH FILM IS RECOMMENDED TO WATCH ON WEEKDAYS

weekdays = [" Mon", " Tue", " Wed", " Thu", " Fri"]
weekends = [" Sat", " Sun"]

# algorithm for finding which films are better to watch on weekdays
moviesDays = []
for i in filmsList:
    probabilityWeekday = 0
    probabilityWeekend = 0
    count = 0
    for x in range(0,40):
        if x != userNumber - 1:
            if context[i][x] != " -":
                count+=1
                if context[i][x] in weekdays:
                    probabilityWeekday += 1
                else:
                    probabilityWeekend += 1
    if (probabilityWeekday/count) > (probabilityWeekend/count):
        moviesDays.append(i)

# we need to recommend just one film for watching in weekday from first part of homework films list
# (if it is possible)

userAverage = usersAverage[userNumber - 1]
flagEmpty = True
for x in rangeMovies:
    if x[0] in moviesDays and abs(x[1] - userAverage) > 0 and flagEmpty:
        flagEmpty = False
        recommendedMovie = x[0]

#flagEmpty = True
if not flagEmpty:
    print("movie that is recommended to watch",recommendedMovie)
else:
    print("may be it is better to watch something from your mates' choice: movie is",rnd.choice(additionalMovies) )
for x in rangeMovies:
    print('movie is '+ str(x[0])+':'+ str(round(x[1],3)))

# post request

host = 'https://cit-home1.herokuapp.com/api/rs_homework_1'
header = {'content-type': 'application/json'}

dataRequest = json.dumps({'user': 24, '1':{"movie 12":3.67, "movie 4":3.44, "movie 19":2.543}, '2': {"movie 12":3.6}})
postRequest = requests.post(host, data=dataRequest, headers=header)

print(postRequest)
print(postRequest.json())
