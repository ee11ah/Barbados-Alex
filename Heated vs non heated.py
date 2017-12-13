# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:47:55 2017

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
fig = plt.figure()
for root, dirs, files in os.walk(path):
    for file in files:
        #looks for big nipi files
        if file.startswith('Data'):
            a =os.path.relpath(root) +'\\'
            bb = file
            day = a[17:23]
            day = day
            
            heat = bb.find("heat")
            HEAT = bb.find("HEAT")
            Moudi = bb.find("Moud")
            if heat != -1 or HEAT != -1:
                if Moudi != -1:
                    pass
                else:
                    num = num+1
                    fig = plt.figure(num)
                    a =os.path.relpath(root) +'\\'
                    bb = file
                    a = a+bb
                    df = pd.read_csv(a)
# =============================================================================
#                     df['Temps'] =  df['# temperatures']
#                     df['FFS'] = df['ff']
#                     plt.scatter(df.Temps, df.FFS,color="K")
#                     plt.title('Fraction frozen, Barbados' + day)
#                     plt.ylabel('FFS')
#                     plt.xlabel('Temperature degrees celsius')
#                     plt.show()
# =============================================================================
                    sample = bb[5:26]
                    #print bb
                    for root, dirs, files in os.walk(path):
                         for file in files:
                             bb = file
                             date = bb.find(sample)
                             if date != -1 and (HEAT !=-1 or heat != -1):
                                 fig = plt.figure(num)
                                 a =os.path.relpath(root) +'\\'
                                 bb = file
                                 a = a+bb
                                 df = pd.read_csv(a)
                                 df['Temps'] =  df['# temperatures']
                                 df['FFS'] = df['ff']
                                 plt.scatter(df.Temps, df.FFS, label = bb)
                                 plt.title('Fraction frozen, Barbados' + day)
                                 plt.ylabel('FFS')
                                 plt.xlabel('Temperature degrees celsius')
                                 legend = fig.legend()
                                 frame = legend.get_frame()
                                 frame.set_facecolor('0.90')
                                 for label in legend.get_texts():
                                    label.set_fontsize('large')
                                 for label in legend.get_lines():
                                    label.set_linewidth(1.5)
                                 fig.savefig('Effect of heating with (ul)' + day)
# =============================================================================
#                              else:
#                                  fig = plt.figure(num)
#                                  a =os.path.relpath(root) +'\\'
#                                  bb = file
#                                  a = a+bb
#                                  df = pd.read_csv(a)
#                                  df['Temps'] =  df['# temperatures']
#                                  df['FFS'] = df['ff']
#                                  plt.scatter(df.Temps, df.FFS,color="B")
#                                  plt.title('Fraction frozen, Barbados' + day)
#                                  plt.ylabel('FFS')
#                                  plt.xlabel('Temperature degrees celsius')
# =============================================================================
            else:
                pass
plt.show()

# =============================================================================
#                         if Blan != -1 or blank != -1 or Blank != -1:
#                             #c = df.index +1
#                             #cc = len(df.Temps)
#                             #df['FFS'] = c/cc
#                             plt.scatter(df.Temps, df.FFS,color="K")
#                             plt.title('Fraction frozen, Barbados' + day)
#                             plt.ylabel('FFS')
#                             plt.xlabel('Temperature degrees celsius')
# =============================================================================    


            #plt.show()