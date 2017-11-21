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
        #looks for big nipi files
        if file.startswith('big'):
            a =os.path.relpath(root) +'\\'
            bb = file
            a = a+bb
            #appends file name to a list for later use
            BigNfiles.append(a)
            #adds the column titles
            df = pd.read_csv(a, names = ["Temps", "?"])
            #gets len of the column for calculation
            b = len(df.Temps)
            #uses index number to get event numbers
            c= df.index +1
            #creates new coloumns for calculations
            df['event_number']= c
            df['FFS']=df.event_number/b
            df['NuT/Na']= (b-df.event_number)/b
            df['INP per Liter'] = 0
            #delets unneccesary coloumns
            del df['event_number']
            del df ['?']
            #takes the time from the file names and converts them to a time object for pandas
            df['start time'] = bb[12:14]+ ':' + bb[14:16]
            df['start time'] = pd.to_datetime(df['start time'], format='%H:%M').dt.time
            df['end time'] = bb[17:19] + ':' + bb[19:21]
            df['end time'] = pd.to_datetime(df['end time'], format='%H:%M').dt.time
            

            #df.to_csv(file, delimiter=',')
            
            print df.head()
            

            
    

            
