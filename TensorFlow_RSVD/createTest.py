import numpy as np
import pandas as pd
import sys
import re

file = open('totaltest.txt', 'a')
file.write("user"+","+"item"+','+"rate"+'\n')
for j in range (1,6041):
	with open('movies.txt','r') as f0:
	
		for i in f0:
			tmp=i.split("::")
			
			#if "3952" == tmp[0]:
   				#continue
			file.write(str(j))
			file.write(","+str(tmp[0])+","+str(0)+'\n') 

