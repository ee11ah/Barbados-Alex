#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 21:33:37 2017

@author: Daniel
"""

import shutil
import os
import glob
import pandas as pd
import numpy as np
import datetime as datetime

APSfiles=[]
files =[]
source = 'O://Data Dump//'
Organized = 'O://Barbados_Data//'


os.chdir(source+'//APS//')
APS_files = [i for i in  glob.glob('*APS*')]
APS_dates = [i[0:6] for i in APS_files]
APS_dates= list(set(APS_dates))

os.chdir(Organized)

for i in range(len(APS_dates)):
    
    if not os.path.exists(Organized+APS_dates[i]):
        os.mkdir(Organized+APS_dates[i])
        
    if not os.path.exists(Organized+APS_dates[i]+'//APS//'):
        os.mkdir(Organized+ APS_dates[i]+'//APS//')
    
    
    os.chdir(Organized+APS_dates[i]+'//APS//')
    [shutil.copy ((source+'//APS//'+j),os.getcwd()) for j in APS_files if APS_dates[i] in j]

#%%
df_INPbig=pd.DataFrame()

def INP_calc(x):
    INP = -np.log(1-x)
    return INP

os.chdir(source+'bigN//')

bigN_files = [i for i in  glob.glob('*bigN*.csv*')]
bigN_dates = [i[5:11] for i in bigN_files]
bigN_dates= list(set(bigN_dates))

#%%
for i in range(len(bigN_files)):
    dt_start = datetime.datetime.strptime(bigN_files[i][5:16],'%y%m%d %H%M')
    d_start = datetime.datetime.strptime(bigN_files[i][5:11], '%y%m%d')
    time_end=datetime.datetime.strptime(bigN_files[i][17:21], '%H%M')
    
    if 'ON' in bigN_files[i]:
        dt_end = (datetime.datetime.combine(dt_start.date() + datetime.timedelta(days=1),
                                           time_end.time()))
    else:
        dt_end = (datetime.datetime.combine(dt_start.date(), d_start.time()))
        
    c = dt_end-dt_start
    t_run = divmod(c.days * 86400 + c.seconds, 60)
    runtime=-t_run[0]
    flow = 16.7
    washV = 5
    Vdrop = 0.05
    divisor = Vdrop/washV*flow*runtime

    
   
    if bigN_files== []:
        continue
   
    else:

        f=i
        #print bigN_files[f]
        df_INPbig =pd.read_csv(bigN_files[f], delimiter =',',
                             index_col = False,dtype ={'temp': np.float64}, names=['temp'])
      #  print df_INPbig.head()
        count=len(df_INPbig)
      
       
        Fraction = df_INPbig.groupby('temp').temp.count().sort_index(ascending = False).cumsum()/len(df_INPbig)
        #print Fraction.head()
        df_out = Fraction.apply(INP_calc)
        #print df_out.head()
#%%

  

        
        fdate = bigN_files[i][5:11]
        path = (Organized+fdate+'//').strip()
        if not os.path.exists(Organized+fdate):
            os.mkdir(Organized+fdate)
            
        if not os.path.exists(Organized+fdate+'//bigN//'):
            os.mkdir(Organized+fdate+'//bigN//')
       # print i,bigN_files[i]
        df_out.to_csv(Organized+fdate+'//'+bigN_files[i].strip('.txt'))
        print bigN_files[i]
        print df_out.head()
        #print Organized+fdate+'//'+bigN_files[i].strip('.txt')

