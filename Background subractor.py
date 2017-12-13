# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 11:00:17 2017

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
import math

path = 'C:\\Users\\ee11ah\\Desktop\\Barbados_DataTest\\'
num = 0
fig = plt.figure(num)
Freezing_temps =[]
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
                        a =os.path.relpath(root) +'\\'
                        bb = file
                        a = a+bb
                        df = pd.read_csv(a)
                        df['Temps'] =  df['# temperatures']
                        df['FFS'] = df['ff']
                        blank = bb.find("blank")
                        Blank = bb.find("Blank")
                        Blan = bb.find("Blan")
                        moud = bb.find("Moud")
                        if Moudi != -1:
                            pass
                        if Blan != -1 or blank != -1 or Blank != -1:
                     

                             #c = df.index +1
                             #cc = len(df.Temps)
                             #df['FFS'] = c/cc
                             plt.scatter(df.Temps, df.K,color="K", label = "Blanks")
                             plt.title('Background subtracted vs blanks, Barbados')
                             plt.ylabel('K')
                             plt.xlabel('Temperature degrees celsius')
                             plt.yscale('log')

                            
                        else:
                            sm = -0.461*df.Temps
                            sm = 0.0057*np.exp(sm)
                            df['BKsub']= df.K - sm
                            plt.scatter(df.Temps, df.BKsub, color = "B", facecolors = "none", label = "Background sub data")
                            plt.title('Background subtracted vs blanks, Barbados')
                            plt.ylabel('K')
                            plt.xlabel('Temperature degrees celsius')
                            plt.yscale('log')

        temperature = [-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35]
        blank_K= []
        for i in temperature:
            blank_K.append((0.0057*(np.exp(-0.461*i))))
        plt.plot(temperature, blank_K, color = "R", label = "Blank K value fit")
        plt.title('Background subtracted vs blanks, Barbados')
        plt.ylabel('K')
        plt.xlabel('Temperature degrees celsius')
        plt.yscale('log')




        
        
fig.savefig('backgrounds vs background sub data (ul)')

plt.show()
# =============================================================================
#                          if Blan != -1 or blank != -1 or Blank != -1:
#                              Freezing_temps.append(df.Temps)
#                              
#                          else:
#                              pass
# 
# 
#  with open("Background runs.csv", "wb") as f:
#      writer = csv.writer(f)
#      writer.writerows(Freezing_temps)
#  print Freezing_temps
# =============================================================================

