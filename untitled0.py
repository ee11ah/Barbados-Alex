# -*- coding: utf-8 -*-
"""
Created on Sat Aug 05 12:26:13 2017

@author: useradmin
"""

import glob as glob
import os
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import datetime as datetime
import pandas as pd
topfolder='O:\\Barbados_Data\\'

bigN_list =[]
bigN_data = pd.DataFrame(columns = {'T', 'INP'})


uL_list =[]
uL_data = pd.DataFrame(columns = {'T', 'INP'})


os.chdir(topfolder)
folders = glob.glob('*\\')
loc = []
for i in range(len(folders)):
    os.chdir(topfolder+ folders[i])
    z=folders[i]
    if glob.glob('*bigN*.csv') ==[]:
        continue
    else:
        
        x=[topfolder+ z+ j for j in glob.glob('*bigN*.csv')]
        bigN_list.extend(x)
        
for i in range(len(folders)):
    os.chdir(topfolder+ folders[i])
    z=folders[i]       
        
    if glob.glob('*Data*.csv') ==[]:
        continue
    else:
        
        y=[topfolder+ z+ j for j in glob.glob('*Data*.csv')]
        uL_list.extend(y)

for i in range (len(bigN_list)):
    y=pd.read_csv(bigN_list[i], names=['T', 'INP'])
    bigN_data = bigN_data.append(y, ignore_index = True)
for i in range (len(uL_list)):
    y=pd.read_csv(uL_list[i], names=['T', 'INP'], usecols = [0,1], skiprows=1)
    uL_data = uL_data.append(y, ignore_index = True)
    
    
    

    
    
    
fig =plt.plot()
plt.scatter(bigN_data['T'], bigN_data['INP'])

plt.scatter(uL_data['T'], uL_data['INP'])
plt.yscale('log')
plt.ylim(0.0001,30)