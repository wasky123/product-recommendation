__author__ = 'Administrator'
import pandas as pd
import numpy as np


#a = pd.read_csv(r"users.csv")


my_matrix = np.loadtxt(open("ratings.csv","rb"),delimiter=",",skiprows=0)
print type(my_matrix)