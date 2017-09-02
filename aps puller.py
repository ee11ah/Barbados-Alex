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
import socket
import pickle
import bokeh
from bokeh import mpl
from bokeh.plotting import figure
#from bokeh.io import output_file, show
from bokeh.charts import TimeSeries, output_file, show
#import Organizer

if socket.gethostname() == 'see4-234':
    Organized = 'C:\\Users\\eardo\\Desktop\\Barbados Data\\Barbados_Data\\'
    picdir =  'C:\\Users\\eardo\\Desktop\\Barbados Data\\Pickles\\'
else:
    Organized = 'O:\\Barbados_Data\\'

##THE FOLLOWING SECTION SEARCHES THE FILES, AND THEN PICKLES THE DATA 
#==============================================================================

# os.chdir(Organized)
# x = glob.glob(Organized + '*\\')
# df_APS= pd.DataFrame()
# aps_list=[]
# 
# for i in range (len(x)):
#     try:
#         os.chdir(x[i]+'APS\\')
#         aps_files = glob.glob('*.txt')
#         for f in range(len(aps_files)):
#             aps_list.append(aps_files[f])
#             df_APSreader=pd.read_csv(aps_files[f], delimiter =',', header =6,  usecols = range(4, 56)) 
#             df_APSreader['datetime']=pd.to_datetime (pd.read_csv(aps_files[f], delimiter =',', header =6).iloc[:, 1]+" "+ 
#                         pd.read_csv(aps_files[f], delimiter =',', header =6).iloc[:, 2])
#             df_APS=df_APS.append(df_APSreader)
#     except WindowsError:
#         continue
# df_APS.to_pickle(picdir+('APS'))
# 
#==============================================================================
       #%% 
df_APS = pd.read_pickle(picdir+'APS')   
df_APS['Total'] = df_APS.iloc[:,0:52].sum(axis =1)
df_APS['datetime']=df_APS['datetime']-datetime.timedelta(hours =5)
df_APS.sort_values(by=['datetime'], inplace = True)
df_APS.set_index('datetime',drop =True, inplace =True)
fig, ax1 = plt.subplots()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

line1, = ax1.plot(df_APS.index, df_APS['Total'])
ax1.set_ylabel('APS particles cm$^{-3}$')
ax1.set_xlabel('Date')

resample = df_APS.resample('1H').mean().reset_index()
resample2 = df_APS.resample('1D').mean().reset_index()
resample.to_csv(Organized + 'all_APS.csv')

order = ['Date','Conc']
unaveraged = pd.DataFrame(dict( Conc = df_APS['Total'],Date=df_APS.index)).reindex(columns=order)
one_hr = pd.DataFrame({ 'Date' : resample.datetime,'Conc' : resample.Total}).reindex(columns=order)
daily = pd.DataFrame({ 'Date' : resample2.datetime,'Conc' : resample2.Total}).reindex(columns=order)
#p = TimeSeries(xyvalues, title = 'APS Timeseries', color = 'blue', xlabel = 'Date',
p1 = figure(x_axis_type="datetime",x_axis_label = 'Date', y_axis_label = 'APS concentration \cc', title="APS Data")
p1.line(x= unaveraged.Date, y=unaveraged.Conc, legend ='Raw Data')
p1.line(x=one_hr.Date, y = one_hr.Conc, color = 'red', line_width =3, legend = 'Hourly mean')
p1.line(x=daily.Date, y = daily.Conc, color = 'black', line_width =3, legend ='Daily mean' )
output_file(Organized+'APS_total.html')
show(p1)

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
