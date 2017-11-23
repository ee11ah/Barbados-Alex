# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:21:45 2017

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

folder = 'C:\Users\ee11ah\Desktop\Barbados_Data_Test\\'
for root, dirs, files in os.walk(folder):
        for file in files:
        #Created files
            plt.figure(1)
            if file.startswith('NEW'):
                a =os.path.relpath(root) +'\\'
                bb = file
                a = a+bb
                df = pd.read_csv(a)
                blan = bb.find("Blan")
                blank =bb.find("blan")
                if blan != -1 and blank != -1:
                    plt.figure(1)
                    plt.scatter(df.Temps, df.FFS)
                    plt.title('FFS vs Data comparison')
                    plt.ylabel('FFS')
                    plt.xlabel('Temperature degrees celsius')
                    getdate: bb[16:20]
                    for root, dirs, files in os.walk(folder):
                        for file in files:
                            if file.startswith('NEW'):
                                a =os.path.relpath(root) +'\\'
                                bb = file
                                a = a+bb
                                mtdate = bb.find(getdate)
                                if mtdate != -1:
                                     plt.scatter(df.Temps, df.FFS)
                                     plt.title(bb + 'vs blank)
                                     plt.ylabel('FFS')
                                     plt.xlabel('Temperature degrees celsius')
                                     getdate: bb[16:20]
                                    
                    
                    
                else:
                    plt.scatter(df.Temps, df.INP)
                    plt.title('INP per liter Barbados')
                    plt.ylabel('INP per liter')
                    plt.yscale('log')
                    plt.xlabel('Temperature degrees celsius')
plt.show(1)