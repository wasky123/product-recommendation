import csv
import operator
import math
import random
import numpy as np
from sets import Set
from numpy import genfromtxt, savetxt
from sklearn import cross_validation
from sys import argv
 
f = open("Automotive.csv")
ratings_data = csv.reader(f)
listData = list(ratings_data)




userRatings = {}
#test Amazon 10 ids
testIdlist = []
# User list without dictionary of movies and ratings 
users = sorted(listData, key=operator.itemgetter(0))
t = open("AutomotiveId.csv")
listt = list(csv.reader(t))
for i in range (0,len(listt)):
	testIdlist.append(listt[i])
#print(users)
# mapping each user's movie preferences
count = 0
u_prev = 0;
#build dictionary of {'user':{'movie1':4,'movie2':3 ...}}
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

# Mapping each movie ranked by users. Transposing userRatings for item based recommendations 
def transposeRankings(ratings):
	transposed = {}
	for user in ratings:
		for item in ratings[user]:
			transposed.setdefault(item, {})
			transposed[item][user] = ratings[user][item]
	
		
	return transposed


#Calculating similarity using Pearson Correlation Similarity 
def sim_pearson(ratings, user_1, user_2):
	similarity = {}
	for item in ratings[user_1]:
		if item in ratings[user_2]:
			similarity[item] = 1

	#calculate the number of similarities 
	numSim = len(similarity)

	# If there is no similarity between them, return 0
	if numSim == 0:
		return 0

	# Add the ratings from users
	userOneSimArray = ([ratings[user_1][s] for s in similarity])
	userOneSimArray = map(float, userOneSimArray)

	sum_1 = sum(userOneSimArray)

	userTwoSimArray = ([ratings[user_2][s] for s in similarity])
	userTwoSimArray = map(float, userTwoSimArray)

	sum_2 = sum(userTwoSimArray)

	# Sum up the squares 

	sum_1_sq = sum([pow(float(ratings[user_1][item]),2) for item in similarity])
	sum_2_sq = sum([pow(float(ratings[user_2][item]),2) for item in similarity])

	# Sum of the products
	productSum = sum([float(ratings[user_1][item]) * float(ratings[user_2][item]) for item in similarity])
	num = productSum - (sum_1*sum_2/numSim)
	den = math.sqrt((sum_1_sq - pow(sum_1,2)/numSim) * (sum_2_sq - pow(sum_2,2)/numSim))

	if den == 0:
		return 0
	r = num / den
	return r

# Calculating Jaccard Similarity 
def compute_jaccard_similarity(ratings, user_1, user_2):
	# similarity = {}
	# for item in ratings[user_1]:
	# 	if item in ratings[user_2]:
	# 		similarity[item] = 1

	# numSim =len(similarity)

	# if numSim == 0:
	# 	return 0

	userOneRatingsArray = ([ratings[user_1][item] for item in ratings[user_1]])
	userOne = set(userOneRatingsArray)
	userTwoRatingsArray = ([ratings[user_2][item] for item in ratings[user_1]])
	userTwo = set(userTwoRatingsArray)

	return (len(set(userOne.intersection(userTwo))) / float(len(userOne.union(userTwo))))

# Calculating Cosine Similarity 
def compute_cosine_similarity(ratings, user_1, user_2):
	similarity = {}
	for item in ratings[user_1]:
		if item in ratings[user_2]:
			similarity[item] = 1

	numSim =len(similarity)

	if numSim == 0:
		return 0

	userOneRatingsArray = ([ratings[user_1][s] for s in similarity])
	userOneRatingsArray = map(float, userOneRatingsArray)
	userTwoRatingsArray = ([ratings[user_2][s] for s in similarity])
	userTwoRatingsArray = map(float, userTwoRatingsArray)
	

	sum_xx, sum_yy, sum_xy = 0,0,0

	for i in range(len(userOneRatingsArray)):
		x = userOneRatingsArray[i]
		y = userTwoRatingsArray[i]

		sum_xx += x*x
		sum_yy += y*y
		sum_xy += x*y

	return sum_xy/math.sqrt(sum_xx*sum_yy)

# Similarity calculation
def closeMatches(ratings, person, similarity):
	first_person = person
	scores = [(similarity(ratings, first_person, second_person), second_person) for second_person in ratings if second_person != first_person]
	scores.sort()
	scores.reverse()
	return scores


# Item based collaborative filtering 
def similarItems(ratings, similarity):
	itemList = {}

	itemsRatings = transposeRankings(ratings)
	
	c = 0
	for item in itemsRatings:
		c = c + 1
		# if c%100 == 0:
		# 	print "%d %d" % (c, len(itemsRatings))
		matches = closeMatches(itemsRatings, item, similarity)
		itemList[item] = matches

	return itemList


# Recommendations for a person based on every other person's rankings and weighted ranking 
def userBasedRecommendations(ratings, wantedPredictions, similarity):
	file = open('user1.txt', 'a')
	ranks = {}

	for tuple in wantedPredictions:
		user = tuple[0]
		movieAsked = tuple[1]

		total = {}
		similaritySums = {}

		for second_person in ratings:
			if second_person == user: continue
			s = similarity(ratings,user, second_person)

			if s <= 0: continue

			for item in ratings[second_person]:
				if item not in ratings[user] or ratings[user][item] == 0:
					total.setdefault(item, 0)
					total[item] += int(ratings[second_person][item])*s
					similaritySums.setdefault(item, 0)
					similaritySums[item] += s
					ranks[item] = total[item]/similaritySums[item]
		file.write(str(ranks[movieAsked])+'\n')



def itemBasedRecommendations(ratings, itemToMatch, usernum):
	file = open('auto1.txt', 'a')
	wantedPredictions =[]
	
	for z in range (0,usernum):
		wantedPredictions.append(testIdlist[z])
	
	a = itemToMatch
	c = open("modifyproductId.csv")
	movie = csv.reader(c)
	listMovie = list(movie)
	movieorder = sorted(listMovie, key=operator.itemgetter(0))
	#print(movieorder)
	dic = {}
	#transfer movie into {id : name,type}
	for i in movieorder:
		#dic[i[0]] = i[1]+','+i[2]
		dic[i[0]] = i[1]
	#print(dic)
	for j in range(0,len(wantedPredictions)):
		recommend = []
		uRatings = ratings[wantedPredictions[j][0]]
		scores = {}
		total = {}
		ranks = {}
		# items rated by this user
		for(item, rating) in uRatings.items():
		# items that are similar to this one
			for(similarity,item_2) in a[item]:
			# don't consider if the user has already rated this item
				if item_2 in uRatings: continue
				scores.setdefault(item_2, 0)
				scores[item_2] += similarity*float(rating)

				# sum over similarities
				total.setdefault(item_2,0)
				total[item_2] += similarity
				if total[item_2] == 0: 
					ranks[item_2] = 1
				else:
					ranks[item_2] = scores[item_2]/total[item_2]
		f = zip(ranks.values(),ranks.keys())
		b = sorted(f,reverse = True)	
		recommend.extend([b[0][1],b[1][1],b[2][1],b[3][1],b[4][1]])
		f = []
		b = []		
		print(len(recommend))
		file.write(wantedPredictions[j][0]+',')
		file.write(str(dic[recommend[0]]))
		for k in range (1,5):
			print(dic[recommend[k]])
			file.write(','+str(dic[recommend[k]]))
		file.write('\n')















# combination of item based and used based recommendations. Content - Boosted Collaborative Filtering
def itemBasedRecommendationsForCBCF(ratings, itemToMatch):
	for user in ratings:
		uRatings = ratings[user]
		scores = {}
		total = {}
		ranks = {}


		# items rated by this user
		for(item, rating) in uRatings.items():
		# items that are similar to this one
			for(similarity,item_2) in itemToMatch[item]:
			# don't consider if the user has already rated this item
				if item_2 in uRatings: 
					uRatings[item_2] = uRatings[item_2]
				else:
					scores.setdefault(item_2, 0)
					scores[item_2] += similarity*float(rating)

					# sum over similarities
					total.setdefault(item_2,0)
					total[item_2] += similarity
					if total[item_2] == 0: 
						uRatings[item_2] = 1
					else:
						uRatings[item_2] = scores[item_2]/total[item_2]
		
	return ratings

#[["3371","673"],["5953","3082"]]


simItems = similarItems(userRatings,compute_cosine_similarity)
#aver = averagescore(userRatings,'3')
#print(aver)
usernum = len(listt)
itemBasedRecommendations(userRatings,simItems,usernum)
print('End of Recommendation')
 #itemBasedRecommendations(userRatings, simItems, toBeRatedList)
# userBasedRecommendations(userRatings, toBeRatedList, compute_cosine_similarity)
# userBasedRecommendations(userRatings, toBeRatedList, sim_pearson)
# itemBasedReco = itemBasedRecommendationsForCBCF(userRatings, simItems)
# userRecosBasedOnDenseMatrix = userBasedRecommendations(itemBasedReco, toBeRatedList, compute_cosine_similarity)


