import csv
import operator
import math
import random
import numpy as np
from sets import Set
from numpy import genfromtxt, savetxt
from sklearn import cross_validation
from sys import argv
 
f = open("ratings.csv")
ratings_data = csv.reader(f)
listData = list(ratings_data)

userRatings = {}

# User list without dictionary of movies and ratings 
users = sorted(listData, key=operator.itemgetter(0))

#print(users)
# mapping each user's movie preferences
count = 0
u_prev = 0;
for u in users:
	userID = u[0]
	movieID = u[1]
	movieRating = u[2]
	if(u_prev == userID):
		userRatings[userID][movieID] = movieRating
		u_prev = userID
	else:
		userRatings[userID] = {}
		userRatings[userID][movieID] = movieRating
		u_prev = userID
#print(userRatings)
#reorder movies.csv !!!
c = open("movies.csv")
movie = csv.reader(c)
listMovie = list(movie)
list1 = []
for i in range(0,len(listMovie)):
	list1.append([int(listMovie[i][0]),listMovie[i][1]])
	
movieorder = sorted(list1)

#file = open('hehe.txt', 'a')
#for i in range(0,len(movieorder)):
	#file.write(str(movieorder[i][0])+','+str(movieorder[i][1])+'\n')

# Mapping each movie ranked by users. Transposing userRatings for item based recommendations 
def transposeRankings(ratings):
	transposed = {}
	for user in ratings:
		for item in ratings[user]:
			transposed.setdefault(item, {})
			transposed[item][user] = ratings[user][item]
	
		
	return transposed
#calculate average score of every movies
def averagescore(ratings):
	file = open('average.txt', 'a')
	a = []
	for i in movieorder:
		a.append(str(i[0]))
	count = {}
	averscore = {}
	b ='not exist'
	list = []
	transposed = transposeRankings(ratings)
	#print (transposed.get('51','not exist'))
	#print(type(transposed[movieid]))
	for j in range(0,len(a)):
		if (transposed.get(a[j],'not exist')==b):continue
		for item in transposed[a[j]]:
			list.append(transposed[a[j]][item])
		#print(list)
		count[a[j]] = str(len(list))
		for k in range (0,len(list)):
			list[k] = int(list[k])
		averscore[a[j]] = str(float(sum(list))/len(list))	
		file.write(str(a[j])+','+count[a[j]]+','+averscore[a[j]]+'\n')

	
averagescore(userRatings)
