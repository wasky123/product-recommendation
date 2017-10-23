__author__ = 'Administrator'
import csv
import operator
import math
# load data
f = open("movies.csv")
movies_data = csv.reader(f)
movie_list = list(movies_data)
movie_dic = {}
# create movie
for m in movie_list:
    movie_dic[m[0]] = m[1]
rec = [('597', 5.0), ('587', 5.0), ('2771', 5.0), ('1265', 5.0), ('3536', 5.0)]
#rec = [('597', 5.0)]
fin = []
print "TOP 15 Movies:"
for i in range(len(rec)):
    if movie_dic.has_key(rec[i][0]):
        #fin.append(movie_dic[rec[i][0]])
        print movie_dic[rec[i][0]]

