import pandas as pd
import math
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

    return (sum / (math.sqrt(sumSqrtX) * math.sqrt(sumSqrtY))).real

# cos metric for context.csv
def simDays(x, y):
    sum = 0
    sumSqrtX = 0
    sumSqrtY = 0
    for i in range(1, 31):
        if context[i][x] != -1 and context[i][y] != -1:
            sum += context[i][x] * context[i][y]
            sumSqrtX += pow(context[i][x], 2)
            sumSqrtY += pow(context[i][y], 2)

    return sum / (math.sqrt(sumSqrtX) * math.sqrt(sumSqrtY))


# read files
data = pd.read_csv("data.csv", sep=",", skiprows=[0], header=None)
context = pd.read_csv("context.csv", sep=",", skiprows=[0], header=None)

# FIRST PART OF HOMEWORK: TO CALCULATE RATING FOR NOT RATED FILMS

# film - i-index
# user - j-index (actually j+1)
# 0 - user 1 , 1 - user 2 ...
# calculate the average score for each user

usersAverage = []
for j in range(0, 40):
    average = 0
    films = 0
    for i in range(1, 31):
        if data[i][j] != -1:
            average += data[i][j]
            films +=1
    usersAverage.append(average / films)

# calculate sim for each user
# user 1 : {user 1: .., user 2:.., user 3:.. ...}
# user 2 : {user 1: .., user 2:.., user 3:.. ...}
metric = []
for ix in range(square):
    metric.append({})
    for jy in range(square):
        metric[ix].update({(jy + 1): sim(ix, jy)})

# sort the data to get the list of sim from high to low
sortedDict = sorted(metric[23].items(), key=lambda x: x[1], reverse=True)


# get five appropriate users
# beginning from 1 because 0 is user himself
user = []
# denominator is lower part of fraction in formula
denominator = 0
for x in range(1, 6):
    user.append(sortedDict[x][0])

# list of final movies
movies = {}

filmsList = []
for x in range(1,31):
    if data[x][userNumber-1] == -1:
        filmsList.append(x)


# final rating
ri = 0
for i in filmsList:
    nominator = 0
    denominator = 0
    ri = 0
    for x in user:
        if data[i][x-1] != -1:
            nominator += sortedDict[x][1] * (data[i][x-1] - usersAverage[x-1])
            denominator += abs(sortedDict[x][1])
    ri = (usersAverage[userNumber - 1] + nominator / denominator).real
    movies.update({i:ri})

# sort the data to get the list of sim from high rating to low
rangeMovies = sorted(movies.items(), key=lambda x: x[1], reverse=True)


# SECOND PART OF HOMEWORK: WHICH FILM IS RECOMMENDED TO WATCH ON WEEKDAYS

for j in range(0, 40):
    average = 0
    for i in range(1, 31):
        if context[i][j] == " Mon":
            context[i][j] = 1
        elif context[i][j] == " Tue":
            context[i][j] = 2
        elif context[i][j] == " Wed":
            context[i][j] = 3
        elif context[i][j] == " Thu":
            context[i][j] = 4
        elif context[i][j] == " Fri":
            context[i][j] = 5
        elif context[i][j] == " Sat":
            context[i][j] = 6
        elif context[i][j] == " Sun":
            context[i][j] = 7
        else:
            context[i][j] = -1

# calculate sim for each user
metricDays = []
for ix in range(square):
    metricDays.append({})
    for jy in range(square):
        metricDays[ix].update({(jy + 1): simDays(ix, jy)})


#sort the data to get the list of sim from high to low
sortedDictDays = sorted(metricDays[23].items(), key=lambda x: x[1], reverse=True)

# find 5 more appropriate users
similarUsers = []
for x in range(1, 6):
    similarUsers.append(sortedDictDays[x][0])

# find day (weekend or weekday) for movies that are not marked
moviesDays = []
for i in filmsList:
        probabilityWeekday = 0
        probabilityWeekend = 0
        for x in similarUsers:
            if context[i][x-1] in range(1,6):
                probabilityWeekday += 1
            elif context[i][x-1] in range(6,8):
                probabilityWeekend += 1
        if (probabilityWeekday/5) > (probabilityWeekend/5):
            moviesDays.append(i)


# we need to recommend just one film for watching in weekday from first part of homework films list
# (if it is possible)
flag = False
recommendedMovie = 0
for x in rangeMovies:
    if x[0] in moviesDays and flag == False:
        flag = True
        recommendedMovie = x[0]

for x in rangeMovies:
    print('movie is '+ str(x[0])+':'+ str(round(x[1],3)))

print(recommendedMovie)


# post request

host = 'https://cit-home1.herokuapp.com/api/rs_homework_1'
header = {'content-type': 'application/json'}

dataRequest = json.dumps({'user': 24, '1':{"movie 12":3.616, "movie 4":3.44, "movie 19":2.543}, '2': {"movie 12":3.6}})
postRequest = requests.post(host, data=dataRequest, headers=header)

print(postRequest)
print(postRequest.json())


