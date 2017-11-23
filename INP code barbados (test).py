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
            #df['INP per Liter'] = 0
            #delets unneccesary coloumns
            del df['event_number']
            del df ['?']
            #takes the time from the file names and converts them to a time object for pandas
            df['time sampled'] =((int(bb[17:19])-int(bb[12:14]))*60)-(((int(bb[19:21])))-((int(bb[14:16]))))
            stm=((int(bb[17:19])-int(bb[12:14]))*60)-(((int(bb[19:21])))-((int(bb[14:16]))))
            df['time sampled'] = stm
            df['liters of air']=16.7*stm
            ON=bb.find("ON")
            twoN=bb.find("2N")
            if ON != -1:
                stm=((24*60)-((int(bb[12:14])*60)+int(bb[14:16]))) 
                mte=((int(bb[17:19])*60)+int(bb[19:21]))
                df['time sampled']=stm+mte
                df['liters of air']=16.7*df['time sampled']
            if twoN != -1:
                stm=((24*60)-((int(bb[12:14])*60)+int(bb[14:16]))) 
                mte=((int(bb[17:19])*60)+int(bb[19:21]))
                df['time sampled']=stm+mte+(24*60)
                df['liters of air']=16.7*['time sampled']
            else:
                pass

                    
            #df['start time'] = '20' + bb[5:7] + '-' + bb[7:9] + '-' + bb[9:11] + ' ' + bb[12:14]+ ':' + bb[14:16]
           # df['start time'] = pd.to_datetime(df['start time'])
           # df['end time'] ='20' + bb[5:7] + '-' + bb[7:9] + '-' + bb[9:11] + ' ' + bb[17:19] + ':' + bb[19:21]
            #df['end time'] = pd.to_datetime(df['end time'])
            #gets the time sampled
            #df['time sampled'] = df['end time'] - df['start time']
            #def tt (spilt):
                #split = df['time sampled'].split(':')
                #return int(split[0])*1440 + int(split[1]) + (intsplit([2])*0)
                #df['time sampled'] = tt
            
          
            print bb
            

            #df.to_csv(file, delimiter=',')
            
            print df.head()
            

            
    

            
