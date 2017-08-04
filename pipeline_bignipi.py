#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:47:31 2017

@author: Daniel O'Sullivan
"""
'''

This script relies on the files being organized correctly (see organizer.py)
This script does the following:
1)Grab datetimes from bigNipi files 
2)Pulls APS data with corresponding timestamps in the duration of bigNipi runs. Gets SUM of counts
3)Pulls SMPS data with corresponding timestamps in the duration of bigNipi runs. Gets SUM of counts
4)Gets INP(T) calculated from INP_T script
5) Makes a pretty graph
    
Known issues: 
    a) the current setup relies on there being a bigNipi file in the organized folder, 
otherwise it won't pull the APS-SMPS data. Also, SMPS and microlitre-nipi 
are not operational yet
    b) currently, this only works for one INP(T)    
    
    
'''    
import socket
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import os
import matplotlib.dates as mdates
import matplotlib.patches as patches
from datetime import datetime
import datetime as dt
import Organizer

#barbados
indir = 'C:\\Users\\useradmin\\Desktop\\Barbados Data'

degree_sign= u'\N{DEGREE SIGN}'
smps_counter = 0
counter = 0
notes_date=[]
note=[]
notes_loc=[]
host = socket.gethostname()

if host == 'Daniels-MacBook-Air.local':
    indir ="//Users//Daniel//Desktop//farmscripts//test data//"
    indir_INP = indir
    
else:
    indir = 'C:\\Users\\useradmin\\Desktop\\Farm\\Formatted Correctly\\'
    indir_INP = '\\Users\\useradmin\\Desktop\\Farmscripts\\'
    out_folder='C:\\Users\\useradmin\\Desktop\\Farmscripts\\'

indir = 'O:\\Barbados_Data\\'
indir_INP = indir

a= glob.glob(indir+'/*/')
df_summary=pd.DataFrame(columns = {'start_datetime', 'end_datetime',
                                    'APS_count', 'SMPS_count'})
dict_INPs={}
df_meta=pd.DataFrame() #df_meta is a sort of 'overview' dataframe
df_smps=pd.DataFrame()
df_APS=pd.DataFrame(columns =[  u'<0.523', u'0.542',
       u'0.583', u'0.626', u'0.673', u'0.723', u'0.777', u'0.835', u'0.898',
       u'0.965', u'1.037', u'1.114', u'1.197', u'1.286', u'1.382', u'1.486',
       u'1.596', u'1.715', u'1.843', u'1.981', u'2.129', u'2.288', u'2.458',
       u'2.642', u'2.839', u'3.051', u'3.278', u'3.523', u'3.786', u'4.068',
       u'4.371', u'4.698', u'5.048', u'5.425', u'5.829', u'6.264', u'6.732',
       u'7.234', u'7.774', u'8.354', u'8.977', u'9.647', u'10.37', u'11.14',
       u'11.97', u'12.86', u'13.82', u'14.86', u'15.96', u'17.15', u'18.43',
       u'19.81', u'datetime'])
df_APSreader=pd.DataFrame(columns =[  u'<0.523', u'0.542',
       u'0.583', u'0.626', u'0.673', u'0.723', u'0.777', u'0.835', u'0.898',
       u'0.965', u'1.037', u'1.114', u'1.197', u'1.286', u'1.382', u'1.486',
       u'1.596', u'1.715', u'1.843', u'1.981', u'2.129', u'2.288', u'2.458',
       u'2.642', u'2.839', u'3.051', u'3.278', u'3.523', u'3.786', u'4.068',
       u'4.371', u'4.698', u'5.048', u'5.425', u'5.829', u'6.264', u'6.732',
       u'7.234', u'7.774', u'8.354', u'8.977', u'9.647', u'10.37', u'11.14',
       u'11.97', u'12.86', u'13.82', u'14.86', u'15.96', u'17.15', u'18.43',
       u'19.81', u'datetime'])

   #1)Grab datetimes from bigNipi files
def get_data(dayfolder):
    os.chdir(dayfolder)
    b=glob.glob('bigN*.csv')##
    missing_NIPI=[]
    global smps_counter, counter,df_smps
    global df_meta, notes_loc, notes_date, notes
    global dict_INPs, b
    if b==[]:
        no_bigN=1
    else:
        no_bigN=0
    if not a:
        no_data_flag=1
        print 'NIPI *Data.CSV files missing {}'.format(analysis_day)
        missing_NIPI.append(analysis_day)
    else:    
        no_data_flag=0
        
        for i in range(len(b)):
            print b
            #start= a[i][5:11]+"_"+a[i][12:16]
            #end = a[i][5:11]+"_"+a[i][17:21]
            start= b[i][5:11]+"_"+b[i][12:16]
            end = b[i][5:11]+"_"+b[i][17:21]
            print b[i][17:21]
            start_datetime = datetime.strptime(start, '%y%m%d_%H%M')
        
            end_datetime =  datetime.strptime(end, '%y%m%d_%H%M')
            
            if 'ON' in b[i]:
                end_datetime = (end_datetime + dt.timedelta(days=1))
                print 'ON in filename'
            else:
               end_datetime =  datetime.strptime(end, '%y%m%d_%H%M')
            print ('end datetime is {}').format(end_datetime)   
            global end_datetime, dt_end
            df_meta= df_meta.append(pd.DataFrame({'start':[start_datetime], 'end':[end_datetime]}),ignore_index = True)
            
            dict_INPs[start_datetime]=pd.read_csv(b[i], delimiter =",", header =0)
            cols=df_meta.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df_meta=df_meta[cols]
            #print df_meta
            global df_meta,B
      
    notes_loc = glob.glob(dayfolder+'/*note*.txt')
    for i in range(len(notes_loc)):

        if notes_loc[i] == []:
            continue
        else:
            text_read= open(notes_loc[0],'r')
           
            
            notes_date.append(datetime.strptime(
                    [notes_loc[0].replace(dayfolder,"")][0][0:6], '%y%m%d %h%M'))
            note.append(text_read.read())
           # print ('comment is {}'.format(note[i]))
    
            

   
#APS SECTION
#2)Pulls APS data with corresponding timestamps in the duration of bigNipi runs. Gets SUM of counts

    
    os.chdir(dayfolder+'APS')
    #print os.getcwd()
    global df_APS, df_out
    x=glob.glob('*.txt')
    for i in range(len(x)):
        #print x[i]
        df_APSreader=pd.read_csv(x[i], delimiter =',', header =6).iloc[:, 4:56] 
#%%
        df_APSreader['datetime']=pd.to_datetime (pd.read_csv(x[i], delimiter =',', header =6).iloc[:, 1]+" "+
          pd.read_csv(x[i], delimiter =',', header =6).iloc[:, 2])
        df_APS=df_APS.append(df_APSreader)
    cols=df_APS.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_APS=df_APS[cols]
    df_APS['datetime'] = (df_APS['datetime'] + dt.timedelta(hours=-5))
#Get the SUM
    apsavs=pd.DataFrame()
    aps_total =pd.DataFrame()
    missing_aps=[]
    #x=pd.DataFrame({'x':0})
    for i in range(len(df_meta)):
        
        
        aps_mask=  (df_APS['datetime'] > df_meta['start'][i]) & (df_APS['datetime'] <=  df_meta['end'][i])
        if df_APS.loc[aps_mask]['datetime'].empty:
            #print 'aps mask not working'
            #apsavs.append(pd.DataFrame(x))
            continue
        
        else:
            
             apsavs = apsavs.append(df_APS.loc[aps_mask].sum(axis=0), ignore_index=True)
             
    
    frames1 = [apsavs, df_meta]
    print no_bigN
    if no_bigN ==1:

        pass
    else:
        #print 'else'
        apsavs = pd.concat (frames1, axis =1, ignore_index= False, join= 'outer')
        aps_total= aps_total.append(apsavs.sum(axis=1),ignore_index=True)
        #print aps_total
        cols=apsavs.columns.tolist()
        cols = cols[-2:] + cols[:-2]
        apsavs = apsavs[cols]
        df_meta['APS']= aps_total.T
         
#SMPS Section
#3)Pulls SMPS data with corresponding timestamps in the duration of bigNipi runs. Gets SUM of counts
#%%

    missing_smps=[]
    if 'SMPS' in os.listdir(dayfolder):
       
        counter +=1
        
        df_smps = pd.DataFrame()
        os.chdir(dayfolder+'SMPS')
        z=glob.glob('*.csv')
        
        if not z:
            print 'SMPS CSV files missing {}'.format(analysis_day)
            missing_smps.append(analysis_day)
            pass
           # df_smps = df_smps.append(x, ignore_index=True)
        else:
            for i in range(len(z)):
                df=pd.read_csv(z[i], delimiter =',', header =25, skipfooter=30, engine = 'python')
                df=df.drop(df.index[2:8])
                
    
                df = df.transpose()
                
                df.columns = df.iloc[0][:]
                df=df.drop(df.index[0])
                df['datetime']=pd.to_datetime(df['Date']+" "+df['Start Time'])
                df=df.drop(['Date', 'Start Time'], axis =1)
                
                df_smps = df_smps.append(df, ignore_index=True)
                
                datetimes = df_smps['datetime']
               #print datetimes
            df_smps.drop('datetime', axis =1, inplace = True)
            df_smps = df_smps.iloc[:,1:].astype(float)
            df_smps.insert(0,'datetimes', datetimes)
           # df_smps.iloc[0:, 1:] = df_smps.iloc[0:, 1:].astype(float)
#%%
#Averaging (should be SUM????)
    smps_avs = pd.DataFrame()
    smps_total=pd.DataFrame()
    
    for i in range (1,2):
        
        #print "length df_meta is {}".format(len(df_meta))
       
        #print "number of cycles is {}".format(i) 
        if df_smps.empty:
            continue
        else: 
            smps_mask = (df_smps['datetimes'] > df_meta['start'][i]) & (df_smps['datetimes']  <=  df_meta['end'][i])
            
        if df_smps.loc[smps_mask]['datetimes'].empty:    
            continue
        else:
            smps_avs=smps_avs.append(df_smps.loc[smps_mask].mean(axis=0, skipna = True), ignore_index=True)
            
           
    smps_total = smps_total.append(smps_avs.sum(axis=1), ignore_index=True).T
    #print smps_total
    smps_total.columns=['SMPS_total']
    
    cols=smps_avs.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    smps_avs = smps_avs[cols]
    df_meta['SMPS']= smps_total
            
            #print "smps total count is {}".format(smps_total.tail(1))
                 #print 'Warning: SMPS averages is zero for {}'.format(dayfolder)
    
    return (df_meta)
#%%   LOOPS get_data function         

df_out = pd.DataFrame()
for i in range(len(a)):
    
    dayfolder=a[i]
    print ('Analyzing {}').format(datetime.strftime(datetime.strptime(a[i][17:23],'%y%m%d'),'%d-%m-%y'))
    analysis_day =datetime.strftime(datetime.strptime(a[i][17:23],'%y%m%d'),'%d-%m-%y')
    os.chdir(dayfolder)
    df_meta=pd.DataFrame()
    
    #pdb.set_trace()
    print dayfolder
    get_data(dayfolder)
    df_out=df_out.append(df_meta)
#%%
#==============================================================================
# missing_aps =[]
# for i in range(len(a)):
#     dayfolder=a[i]
#     get_data(dayfolder)
#==============================================================================
    


#%%

os.chdir(indir_INP)
INPs = pd.read_csv('bigN_INPs.csv',delimiter =',')
#INPs.dropna(axis =0, inplace = True)
#INPs.dropna(axis =0, inplace = True)
temps = INPs.columns.values[2:]
def timefix(time):
    
    correct_time = datetime.strptime(str((time)), '%Y-%m-%d %H:%M:%S')
    return correct_time
# 4)Gets INP(T) calculated from INP_T script

    
INPs['start']=INPs['start'].apply(timefix)
INPs['end_date']=INPs['end_date'].apply(timefix)

df_out.reset_index(inplace = True)

df_INP=pd.DataFrame()
#for i in range(len(df_out)):
for i in range(len(df_out)):
        INP_mask=  (INPs['start'] == df_out['start'][i]) & (INPs['end_date'] ==  df_out['end'][i])
        if INPs.loc[INP_mask].empty:
            print 'empty'
            continue
        
        else:
            
             df_INP = df_INP.append(INPs.loc[INP_mask], ignore_index=True)

if df_INP.empty:
        pass
else:       
    print 'INPs exist!'
    df_INP.set_index('start', inplace =True)
    df_out.set_index('start', inplace =True)
    df_out = df_out.join(df_INP)

#df_out.dropna(axis=0, inplace = True)

#%% 
try:
    df_out['Date']=df_out.start.dt.date
    notes_out =pd.DataFrame ([i for i in zip(notes_date, note)], 
                              columns =['date', 'note'])
    notes_out.date=pd.to_datetime(notes_out.date)
    notes_out.index = notes_out.date
    
    df_out = df_out.drop(u'level_0', errors ='ignore').set_index('Date').join(
            notes_out.set_index('date'),  how ='left')
    df_out.drop(df_out.columns[0], axis =1, inplace =True)
    
except AttributeError:
    pass

old_names= df_out.columns.values[5:]
new_names = [old_names[i] + 'B' for i in range(len(old_names))]
df_out.rename(columns=dict(zip(old_names, new_names)),inplace=True)
df_out.drop(['index','end_date'], axis =1, inplace =True)
df_out.reset_index(inplace =True)

#%%IMPORT uL data
os.chdir(indir_INP)
uL_INPs = pd.read_csv('INPs.csv',delimiter =',')
df_uINP=pd.DataFrame()


for i in range(len(uL_INPs)):
    uL_INPs['start'][i]=datetime.strptime(uL_INPs['start'][i], '%Y-%m-%d %H:%M:%S')
    uL_INPs['end'][i]=datetime.strptime(uL_INPs['end'][i], '%Y-%m-%d %H:%M:%S')
#for i in range(len(df_out)):
for i in range(len(df_out)):
        ulINP_mask=  (uL_INPs['start'] == df_out['start'][i]) & (uL_INPs['end'] ==  df_out['end'][i])
        if INPs.loc[ulINP_mask].empty:
            print 'empty'
            continue
        
        else:
            
             df_uINP = df_uINP.append(uL_INPs.loc[ulINP_mask], ignore_index=True)

if df_uINP.empty:
        pass
else:       
    print 'INPs exist!'
    df_uINP.set_index('start', inplace =True)
    df_out.set_index('start', inplace =True, drop =True)
    df_out = df_out.join(df_uINP, how='left', lsuffix='_left', rsuffix='_right')
    df_out.drop('Unnamed: 0', inplace = True, axis =1)

#%%5) Makes a pretty graph
df_out.sort_index( inplace = True)
#df_APS.set_index('datetime', drop = True, inplace = True)
fig, ax1 = plt.subplots()
ax1.xaxis_date()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

line1, = ax1.plot(df_out.index,df_out['SMPS'], color = 'blue', label ='SMPS count', linestyle ='', marker='.') 
line2, = ax1.plot(df_out.index,df_out['APS'], color = 'green', label ='APS count',marker='.',linestyle =':')
   

#end=np.asarray(df_out['end_left'])
#INP=np.asarray(df_out['INPs'])



ax1.set_ylabel('particles cm$^{-3}$')
ax1.set_xlabel('Date')
ax1.set_ylim(0, 60000)



ax2= ax1.twinx()
dots = ax2.scatter(df_out.index.values, df_out.iloc[:,5].values, color = 'red', label = 'BigNipi @-10 '+degree_sign+'C',s=15 )
dots1 = ax2.scatter(df_out.index.values, df_out.iloc[:,6].values, color = 'blue', label = 'BigNipi @-9 '+degree_sign+'C',s=15 )
dots1 = ax2.scatter(df_out.index.values, df_out.iloc[:,7].values, color = 'black', label = 'BigNipi @-8 '+degree_sign+'C',s=15 )
ax2.set_ylabel('INPs L$^{-1}$')
ax2.set_yscale('log')
ax2.set_ylim(0.1,100)
ax1.legend(frameon= False)
ax2.legend(loc = 'upper right', bbox_to_anchor = (1.05,0.85), frameon =False)


#ax1 = ax1.plot_date(df_out['end'],df_out['INPs'])[0]
#plt.legend(loc = 'upper right', bbox_to_anchor = (0.985,0.85))  

#%%    
#==============================================================================
# from sqlalchemy import create_engine
# import pandas as pd
# engine = create_engine('mysql://root:vercetti85@localhost/barbados')
# connection = engine.connect()
# # if df_out.empty:
#     pass
# 
# else:
#     df_out.to_sql('summary', con = connection, if_exists='replace', index = False)   
# 
# 
# 
# connection.close()
# 
#==============================================================================
