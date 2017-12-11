# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:06:56 2017

@author: ee11ah
"""

path = 'C:\\Users\\ee11ah\\Desktop\\Barbados_Data\\'
num = 0
fig = plt.figure(num)
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
                        df['Temps'] =  df['# temperatures']
                        df['FFS'] = df['ff']
                        blank = bb.find("blank")
                        Blank = bb.find("Blank")
                        Blan = bb.find("Blan")
                        moud = bb.find("Moud")
                        if Blan != -1 or blank != -1 or Blank != -1:
                            pass
                        if moud != -1:
                            pass
                        else:
                            plt.scatter(df.Temps, df.INP)
                            plt.title('fraction frozen, Barbados' + day)
                            plt.ylabel('INP per liter')
                            plt.xlabel('Temperature degrees celsius')
                            plt.yscale('log')
                            
            folder = 'C:\Users\ee11ah\Desktop\Barbados_Data_Test\\'
            for root, dirs, files in os.walk(folder):
                for file in files:
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
                            pass
                        else:
                            plt.scatter(df.Temps, df.INP)
                            plt.title('INP per liter Barbados')
                            plt.ylabel('INP per liter')
                            plt.yscale('log')
                            plt.xlabel('Temperature degrees celsius')
fig.savefig('big NIPI and ul NIPI')
            