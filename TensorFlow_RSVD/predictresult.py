import numpy as np
import pandas as pd
import sys
import csv
import re
f=open('movieId.csv','r')
movie = csv.reader(f)
listMovie = list(movie)

c=open('result.csv','r')
he = csv.reader(c)
ha = list(he)



file = open('predictresult.txt', 'a')
#file.write("user"+","+"item"+','+"rate"+'\n')
for j in range (0,6040):
	for i in range(0,len(listMovie)):
		file.write(str(j+1)+","+str(listMovie[i][0])+','+str(ha[i+j*len(listMovie)][0])+'\n') 
