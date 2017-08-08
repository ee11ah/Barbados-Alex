"""

Created on Mon Aug 17 18:13:19 2015

@author: ed11gcep


Code developed by J. Vergara Temprado & modified by A. Harrison, M. Adams and G. Porter
Contact email eejvt@leeds.ac.uk and ed11gcep@leeds.ac.uk
University of Leeds 2016

"""




"""
READ ME:
    
    To use this code: 
        -Your main folder path should be pasted into line 69. Do not add any more dashes - just make sure there are two at
            the end of the filepath. 
        -Inside your main folder there should be a folder with the date as the name
        -Inside this date folder there should be a folder called 'EF600'
        -Inside the EF600 Folder should be a folder named according to the following convention:
            YYMMDD_MFC2/MFC3/Port/Blan_starttime_endtime_comment_5/6ml_PC/TE
        -Inside your names folder should be four files:
            log.aef
            log.csv
            run
            run.avi
    When running the code:
        -The first questions asks if you want to perform analysis. If you say yes it will take you to the video analysis
        -The code will ask you if you want to analyse runs from a certain day. If you say yes the code will let you know
            whether that run has been analysed yet or if the right files exist
        -When you don't want any more days, press 0 and enter alternating to skim through the rest of the days
        
        -The second question is whether you want to create graphs and files of the data, if you want to plot everything
            just choose the plot all option and all graphs and csv files will be overwritten. 
        -If you want to manually choose which day's data to use, you can use the code to pick days (hold down the enter
            key to choose many consecutive days and runs). But it might be quicker to choose to plot all, and use the
            csv files produced to plot your own in origin. Plotting graphs will produce a large csv file with all of the
            graph's data in the main folder. But will also create csv files for each run inside the date folders which
            can be dragged and dropped into a book in origin so that the csv files form sheets of your book. These can 
            be plotted toegther or separately relatively quickly. To find all the csv files for all the runs, just search
            for '.csv' in your main folder and they should all be in roughly that same place so you can highlight and drag
            into origin.
    To change the code:
        These lines deal with the folder formatting:
            238-275 and 388-418
        These lines deal with the naming conventions:
            420-516
        These lines deal with plotting:
            577-656
        These lines deal with the equations:
            518-571
    If in doubt email Jesus about the video analysis part or Grace about the folder/naming/plotting part
            

"""

import numpy as np
import cv2
from glob import glob
import os
import csv


folder='C:\Users\eempa\Desktop\Barbados\ulNIPI\\' # CHANGE THIS FOLDER - also see bottom of code to alter analysis for wash-off/drop-on
os.chdir(folder)
b=glob('*\\')
b.sort()

def getSec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

def run_video(ini_speed=1,name='Cold Plate',delay=0,temp_frame=0,low_info=0):
    cap = cv2.VideoCapture('run.avi')
                
    print cap.isOpened()
    iframe=1
    events=[]
    speed=ini_speed#ms
    font = cv2.FONT_HERSHEY_SIMPLEX
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    while(cap.isOpened()):
        
        cap.set(cv2.CAP_PROP_POS_FRAMES,iframe)
        ret, frame = cap.read()
        if not ret:
            break
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #print 
        '''
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if iframe>save_frames:
            for j in range(save_frames):
                if j==0:
                    olds[:,:,j]=frame
                else:
                    olds[:,:,j]=olds[:,:,j-1]
        '''
        color=(255,50,0)
        st_events=str(events).strip('[]')
        if not low_info:
            cv2.putText(frame,name,(10,120), font, 1,color,2,cv2.LINE_AA)
            if not isinstance(temp_frame,int):
                cv2.putText(frame,'T= %1.2f C'%temp_frame[iframe],(900,200), font, 2,color,2,cv2.LINE_AA)            
            cv2.putText(frame,'Pause: p - Back: b - Forward: n - Event: spacebar - Delete: d - Faster/play: h,f - Slower: s - 200ms speed: j',(10,25), font, 0.6,color,2,cv2.LINE_AA)
            cv2.putText(frame,'50 frames back: 1 - 10 frames back: 2 - 10 frames forward: 3 - 50 frames forward: 4 - Low info: l',(10,75), font, 0.6,color,2,cv2.LINE_AA)
            cv2.putText(frame,'Frame %i'%iframe,(10,200), font, 2,color,2,cv2.LINE_AA)
            cv2.putText(frame,'Speed %i ms'%speed,(10,300), font, 1,color,2,cv2.LINE_AA)
            cv2.putText(frame,'Events %i'%len(events),(10,400), font, 1,color,2,cv2.LINE_AA)
        else:
            cv2.putText(frame,'Fr %i'%iframe,(10,200), font, 1.5,color,2,cv2.LINE_AA)
            cv2.putText(frame,'Sp %i'%speed,(10,300), font, 0.8,color,2,cv2.LINE_AA)
            cv2.putText(frame,'Ev %i'%len(events),(10,400), font, 0.8,color,2,cv2.LINE_AA)
        if len(st_events)<100:
            cv2.putText(frame,'%s'%st_events,(10,700), font, 0.5,color,2,cv2.LINE_AA)
        else:
            cv2.putText(frame,'%s'%st_events[:100],(10,700), font, 0.5,color,2,cv2.LINE_AA)
            cv2.putText(frame,'%s'%st_events[100:],(10,750), font, 0.5,color,2,cv2.LINE_AA)
        cv2.imshow('Droplet freezing',frame)
        #cv2.waitKey(speed)
        #print iframe
        k = cv2.waitKey(speed)
        if k == 27:         # wait for ESC key to exit
            
            cv2.destroyAllWindows()
            break
        
        elif k == ord(' '): # wait for 's' key to save and exit
            events.append(iframe-delay)
            continue

#            cv2.waitKey(speed)
            

    #    if cv2.waitKey(1) & 0xFF == ord('q'):
    #        break
        elif k == ord('l'):
            low_info=int(np.logical_not(low_info))
            continue
        elif k == ord('s'):
            speed=speed*2
            cv2.waitKey(speed)
        elif k == ord('f'):
            speed=speed/2
            if speed==0:
                speed=1
            cv2.waitKey(speed)
        elif k == ord('h'):
            speed=speed/2
            if speed==0:
                speed=1
            cv2.waitKey(speed)        
        elif k == ord('j'):
            speed=200
        elif k == ord('d'):
            if len(events)!=0:
                
                events.pop()
                continue
            #cv2.waitKey(speed)

        elif k == ord('p'):
            
            cv2.waitKey(0)
        elif k == ord('1'):
            iframe=iframe-50
            continue
        elif k == ord('2'):
            iframe=iframe-10
            continue
        elif k == ord('3'):
            iframe=iframe+10
            continue
        elif k == ord('4'):
            iframe=iframe+50
            continue
            
            
            cv2.waitKey(0)
        elif k == ord('b'):
            iframe=iframe-1
            speed=0
            continue
        '''
        elif k == ord('r'):
            iframe=iframe-save_frames
            for iold in range(save_frames):
                cv2.putText(olds[:,:,save_frames-iold-1],name,(10,100), font, 1,color,2,cv2.LINE_AA)
    
                cv2.putText(olds[:,:,save_frames-iold-1],'Frame %i'%iframe,(10,200), font, 1,color,2,cv2.LINE_AA)
                cv2.putText(olds[:,:,save_frames-iold-1],'Speed %i ms'%speed,(10,300), font, 1,color,2,cv2.LINE_AA)
                cv2.putText(olds[:,:,save_frames-iold-1],'Events %i'%len(events),(10,400), font, 0.5,color,2,cv2.LINE_AA)
                if len(st_events)<10:
                    cv2.putText(olds[:,:,save_frames-iold-1],'%s'%st_events,(10,500), font, 0.5,color,2,cv2.LINE_AA)
                else:
                    cv2.putText(olds[:,:,save_frames-iold-1],'%s'%st_events[:10],(10,500), font, 0.5,color,2,cv2.LINE_AA)
                    cv2.putText(olds[:,:,save_frames-iold-1],'%s'%st_events[10:],(10,600), font, 0.5,color,2,cv2.LINE_AA)
                    
                cv2.imshow('Droplet freezing',olds[:,:,save_frames-iold-1])
                k = cv2.waitKey(500)
                if k == 27:         # wait for ESC key to exit
                    
                    cv2.destroyAllWindows()
                    break
                
                elif k == ord(' '): # wait for 's' key to save and exit
                    events.append(iframe-delay)
                    if first_time:
                        speed=200
                        first_time=0
                    cv2.waitKey(speed)
                iframe=iframe+1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            '''

        
        iframe=iframe+1
    print 
    cap.release()
    cv2.destroyAllWindows()
    return events


#%%
#fig=plt.figure()
#ax=plt.subplot(211)
#bx=plt.subplot()
#%%


print 'Do you want to analyse any data? \n 0: No \n 1: Yes'
ans= (raw_input())
if ans=='1':
    for ifolder in range (len(b)):
        try:
            os.chdir(folder+'\\'+b[ifolder]+'\\EF600')
        except WindowsError:
            print "EF600 Folder not found"
            continue
        if not b[ifolder]== 'blanks\\':
            print 'Analyse Data From Day:  ['+b[ifolder][:-1]+']  Enter:Yes 0:No'
            awnser= (raw_input())
            if awnser=='0':
                continue
        else:
            continue
    
        
        a=glob("*\\")
        a.sort()
        
        for ifile in range(len(a)):
            os.chdir(folder+'\\'+b[ifolder]+'\\EF600\\'+a[ifile])
            if not a[ifile]== 'blanks\\':
                print 'Analyse Data From Run:  ['+a[ifile][:-1]+']  Enter:Yes 0:No'
                if os.path.isfile('events_frame.csv'):
                    print '"events_frame.csv" file existing'
                if os.path.isfile('temps.csv'):
                    print '"temps.csv" file existing'
                if os.path.isfile('ff.csv'):
                    print '"ff.csv" file existing'
                else:
                    print"Not analysed yet"
                awnser= (raw_input())
                if awnser=='0':
                    continue
            else:
                continue
            
            try:
                data=np.genfromtxt('log.csv',delimiter=',',dtype=None)#converters = {1: getSec})
                headers=data[0,:]    
                data=data[1:,:]
                run_times=np.genfromtxt('run',skip_header=1,dtype=None) 
            except IOError:
                print "Sorry, file not found"
                continue
                
            
            temp_frame=np.linspace(0,len(run_times),len(run_times))
            i=0
            for i in range(len(run_times)):
                if run_times[i] in data[:,1]:
                    temp_frame[i]=data[data[:,1].tolist().index(run_times[i]),2]
                else:
                    if int(run_times[i][-1])>0:
                        run_times[i]=run_times[i][:(len(run_times[i])-1)]+str(int(run_times[i][-1])-1)
                    else :
                        run_times[i]=run_times[i][:(len(run_times[i])-1)]+str(int(run_times[i][-1])+1)
                if run_times[i] in data[:,1]:
                    temp_frame[i]=data[data[:,1].tolist().index(run_times[i]),2]
                else:
                    temp_frame[i]=999
        
        
        
            print 'Events input: \n 1: video analisys \n 2: Nevermind(exit)'
            
        
            awnser= (raw_input())
            if awnser=='1':
                
                events=run_video(name=a[ifile][12:][:-1],temp_frame=temp_frame)
                np.savetxt('events_frame.csv',events,delimiter=',')
                print '\'events_frame.csv\' saved/overwritted \n \n'
            if awnser=='2':
                continue
            if awnser==0:
                continue
            else:
                try:
                    events=np.genfromtxt('events_frame.csv',delimiter=',',dtype=None)
                except (IOError,ValueError,TypeError):
                    print"No Values Entered! \n"
                    continue
            events=np.sort(events)

            np.savetxt('events_frame.csv',events,delimiter=',')
            particles=len(events)
            frezz_events=np.linspace(0,len(events),len(events))
            ff=frezz_events/float(particles)
            temps=np.zeros(len(events))
            i=0
            for i in range(len(events)):
                if run_times[int(events[i])] in data[:,1]:
                    temps[i]=data[data[:,1].tolist().index(run_times[int(events[i])]),2]
                else:
                    if int(run_times[int(events[i])][-1])>0:
                        run_times[int(events[i])]=run_times[int(events[i])][:(len(run_times[int(events[i])])-1)]+str(int(run_times[int(events[i])][-1])-1)
                    else :
                        run_times[int(events[i])]=run_times[int(events[i])][:(len(run_times[int(events[i])])-1)]+str(int(run_times[int(events[i])][-1])+1)
                    temps[i]=data[data[:,1].tolist().index(run_times[int(events[i])]),2]
            '''        
                for itime in range(len(data[:,1])):
                    if run_times[pos]==data[itime,1]:
                        print run_times[pos]
                        print data[itime,1]
                        print pos
                        print '---------------'
                        temps[i]=data[itime,2].astype(float)
                        
                        print temps[i]
                        if temps[i]==999:
                            
                            temps[i]=data[:,2].astype(float).min()
                            print 'cambiado',temps[i]
                        i=i+1
                    if temps[i-1]==0:
                        print pos, run_times[pos],data[-1,1],data[0,1]
                '''
            np.savetxt('temps.csv',temps,delimiter=',')
            np.savetxt('ff.csv',ff,delimiter=',')
        
            imp=a[ifile][7:11]
if ans==0:
    pass

import matplotlib.pyplot as plt
import numpy as np
import random

r = lambda: random.randint(0,255)
isbigdata=0
manualpick=0

#print('#%02X%02X%02X' % (r(),r(),r()))
print 'Do you want to make any graphs or create data files? \n 0: No \n 1: Plot All (Alter code to pick plots) \n 2: Pick Manually'
ans= (raw_input())

try:
    os.remove(folder+'Full Graph Data.csv')
except WindowsError:
    print"Could not find file"

if ans=='2':
    manualpick=1
    ans='1'
    pass

if ans=='1':
    os.chdir(folder)
    d=glob('*\\')
    d.sort()
    
    for ifolder in range (len(d)):
        try:
            os.chdir(folder+'\\'+d[ifolder]+'\\EF600')
        except WindowsError:
            print "EF600 Folder not found \n"
            continue
        if manualpick:
            print('\n Graph to include day:  ['+d[ifolder][:-1]+']  Enter: Yes  0: No')
            manpk= (raw_input())
            if manpk=='0':
                continue
        elif not manualpick:
            pass
            
        e=glob("*\\")
        e.sort()
        
        for ifile in range(len(e)):
            os.chdir(folder+'\\'+d[ifolder]+'\\EF600\\'+e[ifile])
            if manualpick:
                print('\n Graph to include run:  ['+e[ifile][:-1]+']  Enter: Yes  0: No')
                manpik=(raw_input())
                if manpik=='0':
                    continue
            elif not manualpick:
                print ("\n " +e[ifile][:-1]+"")
                pass
            
            try:
                inlet=e[ifile][7:][:4]
                filtype=e[ifile][-3:][:2]
                inpc_data=0
                inte_data=0
                ffpc_data=0
                ffte_data=0
                wash=0
                k=0
                isbigdata=0
            except ValueError:
                print ("Your filename: "+e[ifile][:-1]+" is wrong!")
                pass
# THE SECTION BELOW IS WHERE YOU CAN COMMENT OUT INLETS/BLAKS YOU DON'T WANT
            try:

                if 'MFC3'==inlet and filtype=='PC':
                    nameminutes=((int(e[ifile][17:][:2])-int(e[ifile][12:][:2]))*60)-(((int(e[ifile][14:][:2])))-((int(e[ifile][19:][:2]))))
                    volume=5*float(nameminutes)
                    inpc_data=1
                    ffpc_data=1
                    k=1
                    wash=1
                    isbigdata=1
                    
                elif 'MFC2'==inlet and filtype=='PC':
                    nameminutes=((int(e[ifile][17:][:2])-int(e[ifile][12:][:2]))*60)-(((int(e[ifile][14:][:2])))-((int(e[ifile][19:][:2]))))
                    volume=5*float(nameminutes)
                    inpc_data=1
                    ffpc_data=1
                    k=1
                    wash=1
                    isbigdata=1
                    
                elif 'Moud'==inlet:
                    nameminutes=((int(e[ifile][17:][:2])-int(e[ifile][12:][:2]))*60)-(((int(e[ifile][14:][:2])))-((int(e[ifile][19:][:2]))))
                    volume=30*float(nameminutes)
                    inpc_data=1
                    ffpc_data=1
                    inte_data=1
                    ffte_data=1
                    k=1
                    wash=1
                    isbigdata=1
                
                elif 'Port'==inlet:
                    nameminutes=((int(e[ifile][17:][:2])-int(e[ifile][12:][:2]))*60)-(((int(e[ifile][14:][:2])))-((int(e[ifile][19:][:2]))))
                    volume=16.7*float(nameminutes)
                    inpc_data=1
                    ffpc_data=1
                    k=1
                    wash=1
                    isbigdata=1
                    ON=e[ifile].find("ON")
                    twoN=e[ifile].find("2N")
                    if ON != -1:
                        stm=((24*60)-((int(e[ifile][12:][:2])*60)+int(e[ifile][14:][:2])))
                        mte=((int(e[ifile][17:][:2])*60)+int(e[ifile][19:][:2]))
                        nameminutes=stm+mte
                        volume=16.7*float(nameminutes)
                    if twoN != -1:
                        stm=((24*60)-((int(e[ifile][12:][:2])*60)+int(e[ifile][14:][:2])))
                        mte=((int(e[ifile][17:][:2])*60)+int(e[ifile][19:][:2]))
                        nameminutes=stm+mte+(24*60)
                        volume=16.7*float(nameminutes)
                    else:
                        pass

                elif 'MESA'==inlet:
                    nameminutes=((int(e[ifile][17:][:2])-int(e[ifile][12:][:2]))*60)-(((int(e[ifile][14:][:2])))-((int(e[ifile][19:][:2]))))
                    volume=16.7*float(nameminutes)
                    inpc_data=1
                    ffpc_data=1
                    k=1
                    wash=1
                    isbigdata=1
                    ON=e[ifile].find("ON")
                    twoN=e[ifile].find("2N")
                    if ON != -1:
                        stm=((24*60)-((int(e[ifile][12:][:2])*60)+int(e[ifile][14:][:2])))
                        mte=((int(e[ifile][17:][:2])*60)+int(e[ifile][19:][:2]))
                        nameminutes=stm+mte
                        volume=16.7*float(nameminutes)
                    if twoN != -1:
                        stm=((24*60)-((int(e[ifile][12:][:2])*60)+int(e[ifile][14:][:2])))
                        mte=((int(e[ifile][17:][:2])*60)+int(e[ifile][19:][:2]))
                        nameminutes=stm+mte+(24*60)
                        volume=16.7*float(nameminutes)
                    else:
                        pass
                    
                elif 'MESB'==inlet:
                    nameminutes=((int(e[ifile][17:][:2])-int(e[ifile][12:][:2]))*60)-(((int(e[ifile][14:][:2])))-((int(e[ifile][19:][:2]))))
                    volume=16.7*float(nameminutes)
                    inpc_data=1
                    ffpc_data=1
                    k=1
                    wash=1
                    isbigdata=1
                    ON=e[ifile].find("ON")
                    twoN=e[ifile].find("2N")
                    if ON != -1:
                        stm=((24*60)-((int(e[ifile][12:][:2])*60)+int(e[ifile][14:][:2])))
                        mte=((int(e[ifile][17:][:2])*60)+int(e[ifile][19:][:2]))
                        nameminutes=stm+mte
                        volume=16.7*float(nameminutes)
                    if twoN != -1:
                        stm=((24*60)-((int(e[ifile][12:][:2])*60)+int(e[ifile][14:][:2])))
                        mte=((int(e[ifile][17:][:2])*60)+int(e[ifile][19:][:2]))
                        nameminutes=stm+mte+(24*60)
                        volume=16.7*float(nameminutes)
                    else:
                        pass
                    
                elif 'Blan'==inlet and filtype=='PC':
                    #inpc_data=1
                    ffpc_data=1
                    k=1
                    wash=1
                    isbigdata=1
                    
                elif 'Blan'==inlet:
                    #print "\n No Filter type found in name!\n This code will assume it is PolyCarbonate, please change if this is wrong!\n "
                    #inpc_data=1
                    ffpc_data=1
                    k=1
                    wash=1
                    isbigdata=1
                    
            except ValueError:
                print"Your folder is named incorrectly!"
                    
            try:
                
                temperatures=np.genfromtxt('temps.csv',delimiter=',',dtype=str, usecols=0) #adjust usecols as required by csv file
                temperatures=sorted(temperatures, key=float, reverse=True)               
                events=len(temperatures)
            except (IOError, TypeError, ValueError):
                print "Temps file not found"
                continue
            
            try:
                
                #defining function for calculate the radious of a droplet in a filter as function of the contact angle and volume
                def radius_of_droplet(conc_ang,vol=1e-9):
                    #contact angle in degrees. it will convert it
                    #vol in meters^3
                    conc_ang=conc_ang*np.pi/180. 
                    radius=((3*vol)*np.sin(conc_ang)**3/(4*np.pi-np.pi*(2+3*np.cos(conc_ang)-np.cos(conc_ang)**3)))**(1/3.)
                    return radius
                topheader=e[ifile][:-1]
                header='temperatures,INP,ff,K'
                
                """Filter on droplets method"""
                
                ff=np.sort(np.linspace(1,events,events)/float(events))
                contact_angle=110#change this or check 
                Rd=radius_of_droplet(contact_angle)
                R_filter=0.0185892#m
                INP_DoF=np.sort(-np.log(1-ff)*(R_filter**2/Rd**2)/volume) #This is the INP calculation for the droplet on filter method
    
                """Wash off method"""
              
                Fu =np.sort((events - np.linspace(1,events,events))/float(events)) #This is the ff equivalent for the wash off method
                Fu=(np.linspace(1,events,events))/float(events)
                ind=e[ifile].find("ml")
                if ind != -1:
                    washvol = e[ifile][(int(ind)-1)]
                else:
                    print "\n No wash off volume found in name! This code will assume it is 10ml \n"
                    washvol = 10
                    pass
                INP_WO=-np.log(Fu)*(float(washvol)/(0.001*volume))
                
                INP_WO[-1]=np.nan
                INP_WO=np.sort(INP_WO)
                """K-Values"""
                Kval=np.sort((-np.log((1-Fu)))/(0.001)) # Vdrop in cubic cm
                
                data=np.zeros((events,4)) 
                data[:,0]=temperatures
                data[:,2]=ff
                data[:,3]=Kval
    
            except NameError:
                print"\n Your folders are not ordered correctly or your file names are wrong! \n \n"
                continue
    
    
            #INP Graph washoff
    
                
            if ffpc_data:
    
                #FF Graph washoff
                plt.figure(1)
                np.savetxt(folder+'\\'+d[ifolder]+'Data '+e[ifile][:-1]+'.csv',data,header=header,delimiter=',')
                if 'Blan'==inlet:
                    #plt.plot(temperatures,Fu,'d',label=(e[ifile][:-1]),c='w')
                    marker = ['o','d','<','>','*',]       
                    plt.plot(temperatures,Fu,random.choice(marker),label=('_nolegend_'),color="w")
#                    
                else:
                    marker = ['o','d','<','>','*',] 
                    plt.plot(temperatures,Fu,random.choice(marker),label=(e[ifile][:-1]),c='#%02X%02X%02X' % (r(),r(),r()))
                plt.title('Fraction Frozen Curves for Wash-off Technique')
                leg=plt.legend(loc=9,bbox_to_anchor=(1.6,1.025))
                leg.get_frame().set_alpha(0)
                plt.xlabel('Temperature  ($^\circ$C)')
                plt.ylabel('Fraction Frozen')
                plt.savefig(folder+'FF_washoff_plot.png',dpi = 'figure', transparent = True, bbox_inches ='tight')
                print"FF Graph Plotted PC"
            
            if ffte_data:
    
                #FF Graph dropon
                plt.figure(2)
                np.savetxt(folder+'\\'+d[ifolder]+'Data '+e[ifile][:-1]+'.csv',data,header=header,delimiter=',')
                plt.plot(temperatures,ff,'d',label=(e[ifile][:-1]),c='#%02X%02X%02X' % (r(),r(),r()))
                plt.title('Fraction Frozen Curves for Drop-on Technique')
                leg=plt.legend(loc=9,bbox_to_anchor=(1.6,1.025))
                leg.get_frame().set_alpha(0)
                plt.xlabel('Temperature  ($^\circ$C)')
                plt.ylabel('Fraction Frozen')
                plt.savefig(folder+'FF_dropon_plot.png',dpi = 'figure', transparent = True, bbox_inches ='tight')
                print"FF Graph Plotted TE"
            
            if inpc_data:
                #INP Graph Washoff
                data[:,1]=INP_WO
                plt.figure(3)
                np.savetxt(folder+'\\'+d[ifolder]+'Data '+e[ifile][:-1]+'.csv',data,header=header,delimiter=',')     
                marker = ['o','d','<','>','*',]
                plt.plot(temperatures,INP_WO,random.choice(marker),label=(e[ifile][:-1]),c='#%02X%02X%02X' % (r(),r(),r()))
                plt.title('INP concentrations for Wash-off Technique')
                leg=plt.legend(loc=9, bbox_to_anchor=(1.6,1.025))
                leg.get_frame().set_alpha(0)
                plt.xlabel('Temperature  ($^\circ$C)')
                plt.ylabel('$INP  (L^{-1})$')
                plt.yscale('log')
                plt.savefig(folder+'INP_washoff_plot.png', dpi = 'figure', transparent = True, bbox_inches = 'tight')
                print "INP Graph plotted PC"
                
            if inte_data:    
                #INP Graph dropon
                data[:,1]=INP_DoF
                plt.figure(4)
                np.savetxt(folder+'\\'+d[ifolder]+'Data '+e[ifile][:-1]+'.csv',data,header=header,delimiter=',')     
                plt.plot(temperatures,INP_DoF,'o',label=(e[ifile][:-1]),c='#%02X%02X%02X' % (r(),r(),r()))
                plt.title('INP concentrations for Drop-on Technique')
                leg=plt.legend(loc=9, bbox_to_anchor=(1.6,1.025))
                leg.get_frame().set_alpha(0)
                plt.xlabel('Temperature  ($^\circ$C)')
                plt.ylabel('$INP  (L^{-1})$')
                plt.yscale('log')
                plt.savefig(folder+'INP_dropon_plot.png', dpi = 'figure', transparent = True, bbox_inches = 'tight')
                print "INP Graph plotted TE"
            if k:    
                #INP Graph dropon
                data[:,3]=Kval 
                plt.figure(7)
                np.savetxt(folder+'\\'+d[ifolder]+'Data '+e[ifile][:-1]+'.csv',data,header=header,delimiter=',')    
                if 'Blan'==inlet:
                    marker = ['o','d','<','>','*',] 
                    plt.plot(temperatures,Kval,random.choice(marker),label=(e[ifile][:-1]),c='w')
                else:
                    marker = ['o','d','<','>','*',] 
                    plt.plot(temperatures,Kval,random.choice(marker),label=(e[ifile][:-1]),c='#%02X%02X%02X' % (r(),r(),r()))
                plt.title('K Values for fraction frozen')
                leg=plt.legend(loc=9, bbox_to_anchor=(1.6,1.025))
                leg.get_frame().set_alpha(0)
                plt.xlabel('Temperature  ($^\circ$C)')
                plt.ylabel('$K  (cm^{-3})$')
                plt.yscale('log')
                plt.savefig(folder+'K_plot.png', dpi = 'figure', transparent = True, bbox_inches = 'tight')
                print "K Graph plotted"     
                
            
            if isbigdata:
                totaldatafile=open(folder+'Full Graph Data.csv','a')
                totaldata=csv.writer(totaldatafile, delimiter = ',')
                totaldata.writerows(data)
                totaldatafile.close()
                print 'file written'
 
if ans==0:
    print"Try again!"
