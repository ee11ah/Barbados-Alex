# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 15:43:10 2017

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

#read in big nipi data 
path = 'C:\\Users\\ee11ah\\Desktop\\Barbados_Data\\'
num = 0
for root, dirs, files in os.walk(path):
    for file in files:
        #looks for big nipi files
        if file.startswith('Data'):
            a =os.path.relpath(root) +'\\'
            bb = file
            day = a[17:23]
            day = day
            num = num+1
            for root, dirs, files in os.walk(a):
                for file in files:
                    if file.startswith('Data'):
                        fig = plt.figure(num)
                        a =os.path.relpath(root) +'\\'
                        bb = file
                        a = a+bb
                        df = pd.read_csv(a)
                        del df['INP']
                        df['Temps'] =  df['# temperatures']
                        df['FFS'] = df['ff']
                        blank = bb.find("blank")
                        Blank = bb.find("Blank")
                        Blan = bb.find("Blan")
                        if Blan != -1 or blank != -1 or Blank != -1:
                            #c = df.index +1
                            #cc = len(df.Temps)
                            #df['FFS'] = c/cc
                            plt.scatter(df.Temps, df.FFS,color="K")
                            plt.title('Fraction frozen, Barbados' + day)
                            plt.ylabel('FFS')
                            plt.xlabel('Temperature degrees celsius')
                           
                        else:
                            plt.scatter(df.Temps, df.FFS)
                            plt.title('fraction frozen, Barbados' + day)
                            plt.ylabel('FFS')
                            plt.xlabel('Temperature degrees celsius')
                            #fig.savefig('backgrounds vs data ' + day)
            #plt.show()
                        


