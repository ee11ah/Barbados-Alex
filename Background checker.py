# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:07:22 2017

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
#folder = 'C:\Users\ee11ah\Desktop\Barbados_Data\\'
folder = 'C:\Users\ee11ah\Desktop\Barbados_Data_Test\\'
num =0
for root, dirs, files in os.walk(folder):
        for file in files:
        #Created files
            
            #if file.startswith('Data'):
            if file.startswith('NEW'):
                a =os.path.relpath(root) +'\\'
                bb = file
                a = a+bb
                df = pd.read_csv(a)
                #df = pd.read_csv(a, names = ['Temps', 'INP', 'ff', 'K'])
                blank = bb.find("blank")
                Blank = bb.find("Blank")
                Blan = bb.find("Blan")
                if Blan != -1 or blank != -1 or Blank != -1:
                    handling = bb.find("handling")
                    Handling = bb.find("Handling")
                    if handling != -1 or Handling != -1:
                        pass
                    else:
                        dates = bb[14:22]
                        date =dates
                        num = num+1
                        for root, dirs, files in os.walk(folder):
                            for file in files:
                                if file.endswith(dates+'.csv'):
                                    plt.figure(num)
                                    a =os.path.relpath(root) +'\\'
                                    bb = file
                                    a = a+bb
                                    df = pd.read_csv(a)
                                    plt.scatter(df.Temps, df.FFS)
                                    plt.title('INP per liter Barbados' + date)
                                    plt.ylabel('FFS')
                                    plt.xlabel('Temperature degrees celsius')
                                    
                
                #else:
                    #plt.scatter(df.Temps, df.INP)
                    #plt.title('INP per liter Barbados')
                    #plt.ylabel('INP per liter')
                    #plt.yscale('log')
                    #plt.xlabel('Temperature degrees celsius')
#plt.show(1)
