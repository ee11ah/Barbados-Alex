# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 11:20:17 2017

@author: eardo
"""
from datetime import datetime
import os, os.path
import glob
import numpy as np
from os import listdir
import numpy as np
import matplotlib.pyplot as plt
import pylab
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import matplotlib.patches as mpatches
import socket
#import Organizer
host=socket.gethostname()
if host == 'see4-234':
    pickdir = ('C:\\Users\\eardo\\Desktop\\Farmscripts\\Pickels\\')
    indir2 = ('C:\\Users\\eardo\\Desktop\\Farmscripts\\')
    glodir = ('C:\\Users\eardo\\Desktop\\Farmscripts\\glomap data\\160509\\')
    
    
elif host == 'Daniels-MacBook-Air.local':
    
    pickdir = ('//Users//Daniel//Desktop//farmscripts//Pickels//')
    indir2 = ('//Users//Daniel//Desktop//farmscripts//')
    glodir = ('//Users//Daniel//Desktop//farmscripts//glomap data//160509//')
    day_folder='//Users//Daniel//Desktop//farmscripts//test data//'
    out_folder='//Users//Daniel//Desktop//farmscripts//'
    
elif host == 'SEE-L10840':
    pickdir = ('C://Users//useradmin//Desktop//Farmscripts//Pickels//')
    indir2 = ('C://Users//useradmin//Desktop//Farmscripts//')
    glodir = ('C://Users//useradmin//Desktop//Farmscripts//glomap data//160509//')
    day_folder='C:\\Users\\useradmin\\Desktop\\Farm\\Formatted Correctly\\'
    out_folder='C:\\Users\\useradmin\\Desktop\\Farmscripts\\'
    
indir = 'O:\\Barbados_Data\\'
day_folder='O:\\Barbados_Data\\'
out_folder='O:\Barbados_Data\\'


keyword='bigN' 
#==============================================================================
# else:
#     pickdir = ('/Users/Daniel/Desktop/farmscripts/Pickels/')
#     indir2 = ('/Users/Daniel/Desktop/farmscripts/')
#     glodir = ('/Users/Daniel/Desktop/farmscripts/glomap data/160509/')
#==============================================================================

percent = [0.2, 0.5, 0.8]
degree_sign= u'\N{DEGREE SIGN}'
num2words={-10: 'minus 10',-13: 'minus 13', -14 : 'minus 14' ,-15:'minus15',-16:'minus16',-17:'minus17',-18:'minus18',
           -19:'minus19',-20:'minus20',-21:'minus21',
           -22:'minus22', -23:'minus23', -24:'minus24',-25: 'minus25'}

#defining a function


INP=[]
point=[]
paths=[]
fday=[]
day=[]
date=[]
Tlist=[]

# dayp=[]
fdayp=[]
excels_list=[]
time_run=[]
INP_Tlist=[]
start_t=[]
end_t=[]
x=[]
df = pd.DataFrame({'Date':[], 'Start_time':[],'End_time':[], 'INP_T':[]})


"""
This section of the code creates the time series plots, taking data from the
excel files specified and searching for the INP concentration at a specified 
temperature
"""

for name in glob.glob(day_folder+'/*'): 
    if os.path.isdir(name):
        paths.append(name)
    else:
        continue

paths.sort()    
number_days=len(paths)

for T in range(-10,-9):
    
    for i in range(0,2):
        extension = 'csv'
        path=paths[i]
        if not os.path.isdir(path):
            continue
        else:
            os.chdir(path)
            excels = [i for i in glob.glob('*'+keyword+'*.{}'.format(extension))]
            excels_list.append(excels)
            #print(excels)
            number_excels=len(excels)
            if number_excels==0:
                #print('no excels on the '+str(path[-6:]))
                continue
            daily_reading=0
            for i in range(0,number_excels):
                    datain=np.genfromtxt(path+excels[i],delimiter=',',skip_header=1,usecols=(0,1),dtype=float)
                    df=pd.DataFrame(datain, columns = ['T', 'INP'])
                    df2=df.drop_duplicates(['T'], keep = 'last')
                    data=df2.as_matrix()
                    #print(len(data))
                    filename=excels[i]          
                    day.append(path[-6:-4]+'-'+path[-4:-2]+'-'+path[-2:])
                    
                    fday.append(path[-6:-4]+path[-4:-2]+path[-2:]+filename[17:22]+filename[22:26])
                    start_t.append(filename[12:16])
                    end_t.append(filename[18:22])
                    Tlist.append(T)
                    #print(filename)
                    #%%
                    try:
                        filename=int((filename[5:11])+(filename[12:16])+(filename[18:22]))
                    except ValueError:
                        #print(filename)
                        filename='nan'
                        pass
                    time_run.append(filename)
                    try:
                        
                        for i in range(0,len(data)):
                            #print(i)
                            
                            #if Ti/T>1 and Ti-1 >T and Ti+1<T
    
                            #print (data[i,0])
                            #if data[i,0]/T<=1 and data[i-1,0]>=T and data[i+1,0]<=T:
                            try:
                                notequalto = data[i,0]!=data[i+1,0] and data[i,0]!=data[i-1,0]
                                
                            except IndexError:
                                equalto=0
                                pass
                            if data[i,0]/T>=1 and data[i-1,0]>T and data[i+1,0]<T and notequalto==True:
                                #print (data[i,0])
                                point=data[i-1:i+1]                
                                m=(point[1,1]-point[0,1])/(point[1,0]-point[0,0])
                                INP_T=point[0,1]+m*(T-point[0,0])
                                print('INP concentration for'+str(filename)+ '=' + str(INP_T))
                                INP_Tlist.append(INP_T)
                                #print 'added data'+str(INP_T)
                                pass
                            if data[i,0]/T>=1 and data[i-1,0]>T and data[i+1,0]<T and notequalto==False:
                                INP_Tlist.append('triple')
                                pass
                        if data[0,0]<=T:
                            #print(data[0,1])
                            #print('Freezing starts below specified T')
                            #print(data[0,0],'This is the first freezing value')
                            #INP_T=data[0,1]
                            #INP_Tlist.append(INP_T)
                            INP_Tlist.append('below')
                            #print 'added frezbelow'+str(INP_T)
                            pass
            
                        if data[-1,0]>=T:
                            #print(data[-1,1])
                            #print('Freezing ends before specified T')
                            #print(data[-1,0],'This is the last freezing value')
                            #INP_T=data[-1,1]
                            #INP_Tlist.append(INP_T)
                            INP_Tlist.append('before')
                            #print 'added frezends'+str(INP_T)
                            pass
                        
    #                    else:
    #                        INP_Tlist.append('else')
    #                        pass
                    
    
                    except IndexError:
                        #print("Your csv file is empty for this day")
                        INP_Tlist.append('nan')
                
                        continue
                        pass
    
                    if INP_Tlist:
                        x=np.vstack((time_run, start_t))
                        x=np.vstack((x, end_t))
                        x=np.vstack((x, INP_Tlist))
                        x=np.vstack((x, Tlist))
                        x=np.transpose(x)
                        #print x
                        
                    else:
                        continue

    #np.savetxt(day_folder+'INP output.csv',INP_Tlist,delimiter=',')

df3=pd.DataFrame(x, columns = ['Date', 'start', 'end', 'INP', 'T'])
df3=df3[df3!='before'];df3=df3[df3!='below'];
df3['INP']=df3['INP'].astype(float)
df3['T']=df3['T'].astype(float)

#d3=df[df.INP!='inf'] 
#df3.to_csv(out_folder+"INPs.csv")
ax1=df3.plot.scatter(x='T', y='INP', logy=True)
fig = ax1.get_figure()
#fig.savefig(out_folder+keyword+'Binned INP')

df4=(df3.iloc[:,[3,4]]).dropna(how='any')
#df4.to_csv(out_folder+keyword+'.csv')
df5=df4.pivot(index=None, columns='T', values='INP')


ax2=df5.plot.box(logy=True)
fig = ax2.get_figure()
#fig.savefig(out_folder+keyword+'boxplots')

for i in range(len(df3)):
    df3['Date'][i] = datetime.datetime.strptime(df3['Date'][i][0:6],'%y%m%d')
    
for i in range(len(df3)):
    df3['start'][i] = datetime.datetime.combine(df3['Date'][i],datetime.datetime.strptime(df3['start'][i][0:6],'%H%M').time())
    
for i in range(len(df3)):
    df3['end'][i] = datetime.datetime.combine(df3['Date'][i],datetime.datetime.strptime(df3['end'][i][0:6],'%H%M').time())
    
df3.Date
df3.to_csv(out_folder+"bigN_INPs at " +num2words[T]+".csv")
#==============================================================================
# #==============================================================================
# minus15=df5[-15.0].dropna().describe()
# minus16=df5[-16.0].dropna().describe()
# minus17=df5[-17.0].dropna().describe()
# minus18=df5[-18.0].dropna().describe()
# minus19=df5[-19.0].dropna().describe()
# minus20=df5[-20.0].dropna().describe()
# minus21=df5[-21.0].dropna().describe()
# minus22=df5[-22.0].dropna().describe()
# minus23=df5[-23.0].dropna().describe()
# #minus24=df5[-24.0].dropna().describe()
# m#minus25=df5[-25.0].dropna().describe()
# 
# stats=(pd.concat([minus15,minus16,minus17,minus18,minus19,minus20,minus21,minus22,minus23],axis=1)).T
# 
# fig1=plt.plot()
# plt.subplot(111)
# ax3=plt.fill_between(stats.index, stats['25%'],stats['75%'], alpha=0.2)
# plt.yscale('log', nonposy='clip')
# plt.title('25 to 75% confidence intervals for INP data')
# plt.xlabel('T')
# plt.ylabel('INP')
# plt.savefig(out_folder+keyword+'Boxplots')
# INPs = pd.read_pickle(pickdir+'INPs.p')
# #==============================================================================
# 
# #df3.plot.box(x=minus'T', y='INP', logy=True)
# #==============================================================================
# # INPconc=np.genfromtxt(day_folder+'INP output.csv')
# # INPrun=np.genfromtxt(day_folder+'INP run.csv')
# # 
# #==============================================================================
# #==============================================================================
# # for i in range(0,len(fday)):
# #     b=0
# #     a=fday[i]
# #     b=datetime.datetime(int('20'+a[0:2]),int(a[2:4]),int(a[4:6]))
# #     date.append(b) 
# #     c=str(fday[i][6:10])
# #     start_tlist.append(c)
# #     d=str(fday[i][10:14])
# #     end_tlist.append(d)
# # 
# #     
# # x=np.transpose(np.vstack((date, start_tlist, end_tlist, INP_Tlist)))
# # df2=pd.DataFrame(x, columns = ['Date', 'Start_time','End_time', 'INP_T'])
# # df= df.append(df2, ignore_index=True)
# #==============================================================================
# 
# INPs = pd.read_pickle(pickdir+'INPs.p').sort(columns='T')
# INPs2 =INPs.pivot(index=None, columns='T', values='INP')
# 
# df_INP_15 = INPs2[-15.0].describe()
# df_INP_16 = INPs2[-16.0].describe()
# df_INP_17 = INPs2[-17.0].describe()
# df_INP_18 = INPs2[-18.0].describe()
# df_INP_19 = INPs2[-19.0].describe()
# df_INP_20 = INPs2[-20.0].describe()
# df_INP_21 = INPs2[-21.0].describe()
# df_INP_22 = INPs2[-22.0].describe()
# df_INP_23 = INPs2[-23.0].describe()
# df_INP_24 = INPs2[-24.0].describe()
# df_INP_25 = INPs2[-25.0].describe()
# 
# stats=(pd.concat([df_INP_15,df_INP_16,df_INP_16,
#                   df_INP_17,df_INP_18,df_INP_19,df_INP_20,df_INP_21,df_INP_22,df_INP_23, df_INP_24, df_INP_25],axis=1)).T
#     
# fig1=plt.plot()
# plt.subplot(111)
# plt.yscale('log', nonposy='clip')
# plt.xlabel('T')
# plt.ylabel('INP')
# 
# 
# 
#         
# # fig = ax1.get_figure()
# # fig.savefig(out_folder+keyword+'Binned INP')
# # 
# # df4=(df3.iloc[:,[3,4]]).dropna(how='any')
# # df4.to_csv(out_folder+keyword+'.csv')
# # df5=df4.pivot(index=None, columns='T', values='INP')
# # ax2=df5.plot.box(logy=True)
# # fig = ax2.get_figure()
# # fig.savefig(out_folder+keyword+'boxplots')                 
# 
# 
# zero_day = datetime.date(2001,1,1)
# start_day = datetime.date(2001, 9, 15)
# end_day = datetime.date(2001, 10,31)
# 
# 
# felds=pd.read_csv(glodir+'INP_spectra_danny_feldspar.csv', delimiter =',', index_col=0)/1000
# day = list(felds.columns)
# 
# for i in range(len(day)):
#     #day[i]="'"+day[i]+" days'"
#     day[i]=int(day[i])
#     day[i] = datetime.timedelta(day[i])
#     day[i]=day[i]+zero_day
# 
# felds = felds.transpose()
# felds['date']=day
# feld_mask=  (felds['date'] > start_day) & (felds['date'] <=  end_day)
# feld_data=felds.loc[feld_mask]
# 
# feld_data=felds.loc[feld_mask].T.reset_index()
# feld_data['T'] = feld_data['# Temps']*-1
# feld_data=feld_data.T
# feld_data.columns=list(feld_data.loc['T'])
# feld_data.drop('# Temps', inplace = True)
# feld_data.set_index('', inplace =True)
# feld_data.drop('', inplace =True)
# 
# 
# 
# feld_data_stats = pd.DataFrame()
# for i in range (len(list(feld_data.columns))):
#     feld_data_stats[i]=pd.to_numeric(feld_data.iloc[:,i]).describe(percentiles=percent)
# 
# feld_data_stats = feld_data_stats.T
# feld_data_stats.index = feld_data_stats.index*-1
# 
# 
# 
# 
# Nie=pd.read_csv(glodir+'INP_spectra_danny_m3_Niemand.csv', delimiter =',', index_col=0)/1000
# Nie=Nie.transpose()
# Nie['date']=day
# Nie_mask=  (Nie['date'] > start_day) & (Nie['date'] <=  end_day)
# Nie_data=Nie.loc[Nie_mask]
# 
# Nie_data=Nie.loc[Nie_mask].T.reset_index()
# Nie_data['T'] = Nie_data['# Temps']*-1
# Nie_data=Nie_data.T
# Nie_data.columns=list(Nie_data.loc['T'])
# Nie_data.drop('# Temps', inplace = True)
# Nie_data.set_index('', inplace =True)
# Nie_data.drop('', inplace =True)
# 
# 
# 
# Nie_data_stats = pd.DataFrame()
# for i in range (len(list(Nie_data.columns))):
#     Nie_data_stats[i]=pd.to_numeric(Nie_data.iloc[:,i]).describe(percentiles=percent)
# 
# Nie_data_stats = Nie_data_stats.T
# Nie_data_stats.index = Nie_data_stats.index*-1
# 
# 
# total=pd.read_csv(glodir+'INP_spectra_danny_m3_total.csv', delimiter =',', index_col=0)/1000
# total=total.transpose()
# total['date']=day
# total_mask=  (total['date'] > start_day) & (total['date'] <=  end_day)
# 
# total_data=total.loc[total_mask].T.reset_index()
# total_data['T'] = total_data['# Temps']*-1
# total_data=total_data.T
# total_data.columns=list(total_data.loc['T'])
# total_data.drop('# Temps', inplace = True)
# total_data.set_index('', inplace =True)
# total_data.drop('', inplace =True)
# 
# 
# 
# total_data_stats = pd.DataFrame()
# for i in range (len(list(total_data.columns))):
#     total_data_stats[i]=pd.to_numeric(total_data.iloc[:,i]).describe(percentiles=percent)
# 
# total_data_stats = total_data_stats.T
# total_data_stats.index = total_data_stats.index*-1
# 
# marine=pd.read_csv(glodir+'INP_spectra_danny_marine.csv', delimiter =',', index_col=0)/1000
# marine=marine.transpose()
# marine['date']=day
# marine_mask=  (marine['date'] > start_day) & (marine['date'] <=  end_day)
# marine_data=marine.loc[marine_mask]
# 
# marine_data=marine.loc[marine_mask].T.reset_index()
# marine_data['T'] = marine_data['# Temps']*-1
# marine_data=marine_data.T
# marine_data.columns=list(marine_data.loc['T'])
# marine_data.drop('# Temps', inplace = True)
# marine_data.set_index('', inplace =True)
# marine_data.drop('', inplace =True)
# 
# 
# 
# marine_data_stats = pd.DataFrame()
# for i in range (len(list(marine_data.columns))):
#     marine_data_stats[i]=pd.to_numeric(marine_data.iloc[:,i]).describe(percentiles=percent)
# marine_data_stats = marine_data_stats.T
# marine_data_stats.index = marine_data_stats.index*-1
# 
# 
# 
# del marine_mask, total_mask, Nie_mask, feld_mask, felds, total, marine, Nie, day
#     
# 
# os.chdir(indir2)
# indata= np.genfromtxt('all data_1.csv', delimiter = ',')
# 
# fig1=plt.plot()
# plt.subplot(111)
# plt.yscale('log', nonposy='clip')
# plt.xlim(-27, -5)
# plt.ylim(0.001, 50)
# plt.xlabel('T ('+degree_sign+'C)')
# plt.ylabel('INP /L')
# 
# 
# #ax1=plt.fill_between(stats.index, stats['25%'],stats['75%'],  color = 'k', zorder =2)
# ax0 = plt.scatter(indata[:,0], indata[:,1])
# ax1=plt.scatter(INPs['T'], INPs['INP'], color = 'k')
# 
# ax2=plt.fill_between(total_data_stats.index, total_data_stats['20%'],total_data_stats['80%'], alpha = 0.65, color ='b', zorder =1)
# ax3=plt.fill_between(Nie_data_stats.index, Nie_data_stats['20%'],Nie_data_stats['80%'], alpha = 0.65, color = 'r', zorder =0)
# #ax4=plt.fill_between(marine_data_stats.index, marine_data_stats['20%'],marine_data_stats['80%'], alpha = 0.5)
# #ax4=plt.fill_between(feld_data_stats.index, feld_data_stats['20%'],feld_data_stats['80%'], alpha = 0.5)
# 
# red_patch = mpatches.Patch(color='red', label='Niemand')
# blue_patch = mpatches.Patch(color='blue', label='Feldspar + Marine')
# black_patch = mpatches.Patch(color='black', label='Measured')
# 
# plt.legend(handles=[red_patch, blue_patch, black_patch])
# 
# plt.show()
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#==============================================================================
