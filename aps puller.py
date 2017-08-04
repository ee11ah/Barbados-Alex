# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 21:39:13 2017

@author: useradmin
"""
import os 
import pandas as pd
import numpy as np
import glob as glob
import matplotlib.dates as mdates
import datetime
import matplotlib.pyplot as plt
import Organizer

Organized = 'O:\\Barbados_Data\\'
os.chdir(Organized)
x = glob.glob(Organized + '*\\')
df_APS= pd.DataFrame()
aps_list=[]
for i in range (len(x)):
    os.chdir(x[i]+'APS\\')
    aps_files = glob.glob('*.txt')
    for f in range(len(aps_files)):
        aps_list.append(aps_files[f])
        df_APSreader=pd.read_csv(aps_files[f], delimiter =',', header =6,  usecols = range(4, 56)) 
        df_APSreader['datetime']=pd.to_datetime (pd.read_csv(aps_files[f], delimiter =',', header =6).iloc[:, 1]+" "+ 
                    pd.read_csv(aps_files[f], delimiter =',', header =6).iloc[:, 2])
        df_APS=df_APS.append(df_APSreader)    
       #%% 
df_APS['Total'] = df_APS.iloc[:,0:52].sum(axis =1)
df_APS['datetime']=df_APS['datetime']-datetime.timedelta(hours =5)
df_APS.sort_values(by=['datetime'], inplace = True)
df_APS.set_index('datetime',drop =True, inplace =True)
fig, ax1 = plt.subplots()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

line1, = ax1.plot(df_APS.index, df_APS['Total'])
ax1.set_ylabel('APS particles cm$^{-3}$')
ax1.set_xlabel('Date')



#==============================================================================
# #%%df_APS['Total'] = df_APS.iloc[:,0:52].sum(axis =1)
# 
# fig2, ax2 = plt.subplots()
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
# 
# line1, = ax2.plot(test.index, test['Total'])
# ax1.set_ylabel('APS particles cm$^{-3}$')
# ax1.set_xlabel('Date')
#==============================================================================
