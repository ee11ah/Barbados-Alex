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
import matplotlib.pyplot as plt

APSfiles=[]
files =[]
source = 'O://Data Dump//'
Organized = 'O://Barbados_Data//'

uL_start=[]
uL_end=[]
uL_start_list=[]
uL_end_list=[]
big_start=[]
big_end=[]
bigNlocs=[]
uL=[]
uL_dt=[]
#==============================================================================
# os.chdir(source+'//APS//')
# APS_files = [i for i in  glob.glob('*APS*')]
# APS_dates = [i[0:6] for i in APS_files]
# APS_dates= list(set(APS_dates))
# 
# os.chdir(Organized)
# 
# for i in range(len(APS_dates)):
#     
#     if not os.path.exists(Organized+APS_dates[i]):
#         os.mkdir(Organized+APS_dates[i])
#         
#     if not os.path.exists(Organized+APS_dates[i]+'//APS//'):
#         os.mkdir(Organized+ APS_dates[i]+'//APS//')
#     
#     
#     os.chdir(Organized+APS_dates[i]+'//APS//')
#     [shutil.copy ((source+'//APS//'+j),os.getcwd()) for j in APS_files if APS_dates[i] in j]
# 
#==============================================================================
#%%
df_INPbig=pd.DataFrame()

def INP_calc(x):
    INP = -np.log(1-x)
    return INP

os.chdir(source+'bigN//')

bigN_files = [i for i in  glob.glob('*bigN*.csv*')]
bigN_dates = [i[5:11] for i in bigN_files]
bigN_dates= list(set(bigN_dates))

#%%Pulls big N files, calculates INPs
for i in range(len(bigN_files)):
    dt_start = datetime.datetime.strptime(bigN_files[i][5:16],'%y%m%d %H%M')
    d_start = datetime.datetime.strptime(bigN_files[i][5:11], '%y%m%d')
    time_end=datetime.datetime.strptime(bigN_files[i][17:21], '%H%M')
    
    if 'ON' in bigN_files[i]:
        dt_end = (datetime.datetime.combine(dt_start.date() + datetime.timedelta(days=1),
                                           time_end.time()))
    else:
        dt_end = (datetime.datetime.combine(dt_start.date(), time_end.time()))
        
    c = dt_end-dt_start
    t_run = divmod(c.days * 86400 + c.seconds, 60)
    print ('t_run is {}').format(t_run)
    runtime=t_run[0]
    print ('runtime is {}').format(runtime)
    flow = 16.7
    washV = bigN_files[i].find('ml')
    if washV != -1:
        bigN_files[i][(int(washV)-1)] # only single digit numbers for this in name
    else:
        print "\n No wash off volume found in name! \n This code will assume it is 10ml. please change if it is not!\n"
        washV = 10
        pass
    Vdrop = 0.05
    divisor = Vdrop/washV*flow*runtime
    big_start.append(dt_start)
    big_end.append(dt_end)
    
   
    if bigN_files== []:
        continue
   
    else:
        
        f=i
        bigNlocs.append(source+'bigN//'+bigN_files[f])
        #print bigN_files[f]
        df_INPbig =pd.read_csv(bigN_files[f], delimiter =',',
                             index_col = False,dtype ={'temp': np.float64}, names=['temp'])
      #  print df_INPbig.head()
        count=len(df_INPbig)
      
       
        Fraction = df_INPbig.groupby('temp').temp.count().sort_index(ascending = False).cumsum()/len(df_INPbig)
        #print Fraction.head()
        df_out = Fraction.apply(INP_calc)/divisor
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
os.chdir (source + 'uL NIPI//')
uL_folders =[i for i in glob.glob('*//')]

#==============================================================================
# for j in range(len(uL_folders)):
#     os.chdir(source + 'uL NIPI//' + uL_folders[j])
#     analysis_list = [k for k in glob.glob('*Data*.csv')]
#     date_list = [m[5:11]+'//' for m in analysis_list]
#     file_info = [l for l in zip(analysis_list, date_list)]
#     
#     
#     for z in range (len(file_info)):
#         if not os.path.exists(Organized+date_list[z]):
#             os.mkdir(Organized+date_list[z])
#         print z
#         shutil.copy ((os.getcwd()+'\\'+file_info[z][0]),Organized+date_list[z])
#         
#==============================================================================
        
#%% Scans for uL *data files


for i in range(len(bigN_dates)):
    os.chdir(Organized+'//'+ bigN_dates[i])
    c=glob.glob('Data*.csv')##
    missing_uNIPI=[]
        
    if c==[]:
        no_uL=1
    else:
        no_uL=0
    if not c:
        no_data_flag=1
       # print 'uL NIPI *Data.CSV files missing {}'.format(bigN_dates[i])
       # missing_NIPI.append(analysis_day)
    else:    
        no_data_flag=0
        
        for j in range(len(c)):
           
            if 'Blan' in c[j]:
                
                continue

            else:
                
                uL_start= c[j][5:11]+"_"+c[j][17:21]
                uL_end = c[j][5:11]+"_"+c[j][22:26]
             
                uL_start = (datetime.datetime.strptime(uL_start, '%y%m%d_%H%M'))
                uL_start_list.append(uL_start)
                
                uL_end_datetime =  datetime.datetime.strptime(uL_end, '%y%m%d_%H%M')

    
                if 'ON' in c[j]:

                    x= (uL_end_datetime + datetime.timedelta(days=1))
                    uL_end_list.append(x)
                    print 
                    uL.append(Organized+ bigN_dates[i]+'//'+c[j])
                    
                elif '2N' in c[j]:
                    x= (uL_end_datetime + datetime.timedelta(days=2))
                    uL_end_list.append(x)
                    uL.append(Organized+ bigN_dates[i]+'//'+c[j])
       
                else:
                   
                   x=datetime.datetime.strptime(uL_end, '%y%m%d_%H%M')
                   uL_end_list.append(x)
                   uL.append(Organized+ bigN_dates[i]+'//'+c[j])
                   print bigN_dates,c[j]
                   
                   
big_N = pd.DataFrame([[i,j] for i,j in zip(big_start, big_end)])
uL_dt = pd.DataFrame([[i,j] for [i,j] in zip(uL_start_list, uL_end_list)])
bigNlocs=pd.DataFrame(bigNlocs)
    
#%% Checks for uL NIPI and big NIPI taken at the same time
for i in range(len(uL_dt)):
    mask = (uL_dt.iloc[i,0] == big_N.iloc[:,0]) & (uL_dt.iloc[i,1] == big_N.iloc[:,1])
    big = bigNlocs.loc[mask]
    if big.loc[mask].empty:
        continue
        'not found'
        #print('didnt find {}').format(uL_dt[i])
    else:
        print 'hello'
        x=  big_N[mask][1].astype(datetime.timedelta)-big_N[mask][0].astype(datetime.timedelta)
        if bigNlocs.loc[mask].empty:
            pass
        else:
            print 'found'
            c=x.tolist()[0]
            t_run = divmod(c.days * 86400 + c.seconds, 60)
            runtime=t_run[0]
            flow = 16.7
            washV = 5
            Vdrop = 0.05
            divisor = Vdrop/washV*flow*runtime
            bigdata = pd.read_csv(big.iloc[0].tolist()[0], names=['temp'])
            Fraction = bigdata.groupby('temp').temp.count().sort_index(ascending = False).cumsum()/len(bigdata)
            INP=Fraction.apply(INP_calc)/divisor
            fig, ax1 =plt.subplots()
            
            a = ax1.scatter(INP.index, INP.iloc[:],label = big.loc[mask].values[0][0])
            
            
            uL_data = pd.read_csv(uL[i]).drop(labels =['ff','K'], axis =1 )
            ax2 =plt.scatter (uL_data.iloc[:,0], uL_data.iloc[:,1],label = uL[i])
            ax1.set_yscale('log')
            ax1.set_ylim(0.0001, 30)
            plt.legend()
            
            
#==============================================================================
# #%% Scans all folders in organized and plots
# 
# topfolder='O:\\Barbados_Data\\'
# 
# bigN_list =[]
# bigN_data = pd.DataFrame(columns = {'T', 'INP'})
# 
# 
# uL_list =[]
# uL_data = pd.DataFrame(columns = {'T', 'INP'})
# 
# 
# os.chdir(topfolder)
# folders = glob.glob('*\\')
# loc = []
# for i in range(len(folders)):
#     os.chdir(topfolder+ folders[i])
#     z=folders[i]
#     if glob.glob('*bigN*.csv') ==[]:
#         continue
#     else:
#         
#         x=[topfolder+ z+ j for j in glob.glob('*bigN*.csv')]
#         bigN_list.extend(x)
#         
# for i in range(len(folders)):
#     os.chdir(topfolder+ folders[i])
#     z=folders[i]       
#         
#     if glob.glob('*Data*.csv') ==[]:
#         continue
#     else:
#         
#         y=[topfolder+ z+ j for j in glob.glob('*Data*.csv')]
#         uL_list.extend(y)
# 
# for i in range (len(bigN_list)):
#     y=pd.read_csv(bigN_list[i], names=['T', 'INP'])
#     bigN_data = bigN_data.append(y, ignore_index = True)
# for i in range (len(uL_list)):
#     y=pd.read_csv(uL_list[i], names=['T', 'INP'], usecols = [0,1], skiprows=1)
#     uL_data = uL_data.append(y, ignore_index = True)
#      
# fig =plt.plot()
# plt.scatter(bigN_data['T'], bigN_data['INP'])
# 
# plt.scatter(uL_data['T'], uL_data['INP'])
# plt.yscale('log')
# plt.ylim(0.0001,30)            
#             
#             
#==============================================================================



       
   