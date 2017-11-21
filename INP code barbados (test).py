# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 12:03:06 2017

@author: ee11ah
"""

import pandas as pd
from pandas import DataFrame
import datetime
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

BigNfiles = []
#read in big nipi data 
path = 'C:\Users\ee11ah\Desktop\Barbados_Data\\'
for root, dirs, files in os.walk(path):
    for file in files:
        if file.startswith('big'):
            a =os.path.relpath(root) +'\\'
            bb = file
            a = a+bb
            BigNfiles.append(a)
            df = pd.read_csv(a, names = ["Temps", "?"])
            #df['Temps']= df(c0)
            b = len(df.Temps)
            c= df.index +1
            df['event_number']= c
            df['FFS']=df.event_number/b
            df['NuT/Na']= (b-df.event_number)/b
            df['INP per Liter'] = 0
            #df.to_csv(file, delimiter=',')
            
            print c
            print a
            print df.head()
            

            
    

            
