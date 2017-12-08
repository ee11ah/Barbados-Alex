# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 15:09:07 2017

@author: ee11ah
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 14:41:01 2017

@author: ee11ah
"""

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
path = 'C:\\Users\\ee11ah\\Desktop\\Barbados_DataTest\\'
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
            num = num+1
            for root, dirs, files in os.walk(a):
                for file in files:
                    if file.startswith('Data'):
                       
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
                        Moudi = bb.find("Moud")
                        if Moudi != -1:
                            S5 = bb.find("S5")
                            S4 = bb.find ("S4")
                            S3 = bb.find("S3")
                            S2 = bb.find("S2")
                            heat = bb.find("heat")
                            HEAT = bb.find("HEAT")
                            if S5 != -1:
                                plt.scatter(df.Temps, df.FFS,color="K", label = "< 1um")
                                plt.title('MOUDI,Barbados')
                                plt.ylabel('FFS')
                                plt.xlabel('Temperature degrees celsius')
                                # Now add the legend with some customizations.
                                legend = fig.legend()
                                frame = legend.get_frame()
                                frame.set_facecolor('0.90')
                                for label in legend.get_texts():
                                    label.set_fontsize('large')
                                for label in legend.get_lines():
                                    label.set_linewidth(1.5)  # the legend line width
                            if S4 != -1:
                                if HEAT !=-1 or heat != -1:
                                    pass
                                    #plt.scatter(df.Temps, df.FFS,color="B", facecolors = "none", label = "1-1.8um Heated")
                                    #plt.title('MOUDI,Barbados')
                                    #plt.ylabel('FFS')
                                    #plt.xlabel('Temperature degrees celsius')
                                    # Now add the legend with some customizations.
                                    #legend = fig.legend()
                                    #frame = legend.get_frame()
                                    #frame.set_facecolor('0.90')
                                    #for label in legend.get_texts():
                                     #   label.set_fontsize('large')
                                    #for label in legend.get_lines():
                                     #   label.set_linewidth(1.5)  # the legend line width
                                else:
                                    plt.scatter(df.Temps, df.FFS,color="B", label = "1-1.8um")
                                    plt.title('MOUDI,Barbados')
                                    plt.ylabel('FFS')
                                    plt.xlabel('Temperature degrees celsius')
                                    # Now add the legend with some customizations.
                                    legend = fig.legend()
                                    frame = legend.get_frame()
                                    frame.set_facecolor('0.90')
                                    for label in legend.get_texts():
                                        label.set_fontsize('large')
                                    for label in legend.get_lines():
                                        label.set_linewidth(1.5)  # the legend line width
                            if S3 != -1:
                                if HEAT !=-1 or heat != -1:
                                    pass
                                   #plt.scatter(df.Temps, df.FFS,color="G", facecolors = "none", label = "1.8-3.2um Heated")
                                    #plt.title('MOUDI,Barbados')
                                    #plt.ylabel('FFS')
                                    #plt.xlabel('Temperature degrees celsius')
                                    # Now add the legend with some customizations.
                                    #legend = fig.legend()
                                    #frame = legend.get_frame()
                                    #frame.set_facecolor('0.90')
                                    #for label in legend.get_texts():
                                     #   label.set_fontsize('large')
                                    #for label in legend.get_lines():
                                     #   label.set_linewidth(1.5)  # the legend line width
                                else:
                                    plt.scatter(df.Temps, df.FFS,color="G", label = "1.8-3.2um")
                                    plt.title('MOUDI,Barbados')
                                    plt.ylabel('FFS')
                                    plt.xlabel('Temperature degrees celsius')
                                    # Now add the legend with some customizations.
                                    legend = fig.legend()
                                    frame = legend.get_frame()
                                    frame.set_facecolor('0.90')
                                    for label in legend.get_texts():
                                        label.set_fontsize('large')
                                    for label in legend.get_lines():
                                        label.set_linewidth(1.5)  # the legend line width
                            if S2 != -1:
                                if HEAT !=-1 or heat != -1:
                                    pass
                                #if HEAT !=-1 or heat != -1:
                                 #   plt.scatter(df.Temps, df.FFS,color="R", facecolors = "none", label = "3.2-5.6um Heated")
                                  #  plt.title('MOUDI,Barbados')
                                   # plt.ylabel('FFS')
                                    #plt.xlabel('Temperature degrees celsius')
                                    ## Now add the legend with some customizations.
                                    #legend = fig.legend()
                                    #frame = legend.get_frame()
                                    #frame.set_facecolor('0.90')
                                    #for label in legend.get_texts():
                                     #   label.set_fontsize('large')
                                    #for label in legend.get_lines():
                                     #   label.set_linewidth(1.5)  """# the legend line width
                                else:
                                    plt.scatter(df.Temps, df.FFS,color="R", label = "3.2-5.6um")
                                    plt.title('MOUDI,Barbados')
                                    plt.ylabel('FFS')
                                    plt.xlabel('Temperature degrees celsius')
                                    # Now add the legend with some customizations.
                                    legend = fig.legend()
                                    frame = legend.get_frame()
                                    frame.set_facecolor('0.90')
                                    for label in legend.get_texts():
                                        label.set_fontsize('large')
                                    for label in legend.get_lines():
                                        label.set_linewidth(1.5)  # the legend line width
                            
                        if Blan != -1 or blank != -1 or Blank != -1:
                           pass
                        else:
                            pass
                        fig.savefig('Effect of heating with the MOUDI (ul)')
plt.show()
                     