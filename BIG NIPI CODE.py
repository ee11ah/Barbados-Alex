import Tkinter
import tkFileDialog
import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np


helpText = '''Help for IR analyis of cryoplates
Note this software assumes you have a series of csv files exported from the FLUKE InfraRed Camera in a folder.

The first screen asks for the dimensions of the plate.  This should be given relative to points interested in, a 96 well plate for example would be either 12x8 or 8x12.
Time between images is simply to let the x-axis be a realistic number and should be how often you took photos with the IR camera.  For example every 20 seconds.

Second screen asks for the coordinates of the 4 corners of the plate.  The easiest way to do this is to open one of the csv files in Excel/OpenOffice select all the data and conditionally format it as a colourmap/colourscale.
You can then read off the coordinates from the spreadsheet using it's own coordinates rather than Excel's (the first data row/column are coordinates to be used)
The containing folder asks for the root folder where all the csv files are contained, clicking on the button opens a folder browser.

The final screen opens the well selection screen here you can click on individual wells to select them or click and drag a box around a group of wells to select them.  
Holding down control while dragging the box will deselect the contents.
Once finished clicking plot will draw the graph and show it.  In the graph interface you can naviagate round the graph and save the graph to a file.
'''


class App:
    def __init__(self, master):
        '''Initialisation requires a top level Tkinter object passed to it as master.
        Sets up the frames for each screen as well as the canvas.  This is done before hand so objects can be added before changing screen.
        Set up help keybinding as well as moving to the first screen.
        '''
        self.selected = []
        self.master = master
        self.master.wm_title("IR graph plotter")
        self.root = Tkinter.StringVar()
        self.selectFrame = Tkinter.Frame(master, height=800, width=800)
        self.canvas = Tkinter.Canvas(self.selectFrame, height=500, width=800)
        self.optionFrame = Tkinter.Frame(master, height=800, width=800)
        self.selectBox = None
        
        self.master.bind_all("<F1>", self.showHelp)
        
        
        self.optionFrame.grid()
        self.getUserOptions()

    def showHelp(self, event):
        '''Method called from a an event in the main program.  Opens a help window if one isn't open.
        Also binds the Escape key to quit.
        '''
        try:
            self.helpWindow.deiconify()
        except:
            self.helpWindow = Tkinter.Toplevel(self.master)
            self.helpWindow.wm_title("Help")
            self.helpWindow.bind("<Escape>", self.close)
            text = Tkinter.Text(self.helpWindow, height=30, width=100, wrap=Tkinter.WORD)
            text.insert(Tkinter.END, helpText)
            text.config(state=Tkinter.DISABLED)
            text.pack()

    def close(self, event):
        '''Generic quit callback.  Should be called from own window as it destroys parent widget'''
        event.widget.destroy()

    def getUserOptions(self):
        '''First screen shown to user.  Gathers some general infomation before moving onto the actual input.
        Attaches widgets to the optionFrame which is used in the text entry screens.
        '''
        wellAcrossL = Tkinter.Label(self.optionFrame, text="Number of wells across").grid(row=0, column=0, sticky=Tkinter.W)
        self.wellAcross = Tkinter.Entry(self.optionFrame)
        
        wellDownL = Tkinter.Label(self.optionFrame, text="Numer of wells down").grid(row=1, column=0, sticky=Tkinter.W)
        self.wellDown = Tkinter.Entry(self.optionFrame)
        
        sampleTimeL = Tkinter.Label(self.optionFrame, text="Time between images (seconds)").grid(row=2, column=0, sticky=Tkinter.W)
        self.sampleTimeEntry = Tkinter.Entry(self.optionFrame)
        
        submit = Tkinter.Button(self.optionFrame, text="Next", command=self.optionsToInput).grid(row=3, column=2)
        self.wellAcross.grid(row=0, column=1)
        self.wellDown.grid(row=1, column=1)
        self.sampleTimeEntry.grid(row=2, column=1)

    def getUserInput(self):
        '''Screen for entering vial positions, all widgets are attached to optionFrame and gridded into position.
        Folder browser button has own callback attached.
        Next and back buttons are attached to specific callbacks to deal with loading and unloading the frame.
        '''
        colL = Tkinter.Label(self.optionFrame, text="Column").grid(row=0, column=1)
        rowL = Tkinter.Label(self.optionFrame, text="Row").grid(row=0, column=2)
        
        topLeftL = Tkinter.Label(self.optionFrame, text="Top left well").grid(row=1, column=0, sticky=Tkinter.W)
        self.topLeftCol = Tkinter.Entry(self.optionFrame)
        self.topLeftRow = Tkinter.Entry(self.optionFrame)
        
        topRightL = Tkinter.Label(self.optionFrame, text="Top right well").grid(row=2, column=0, sticky=Tkinter.W)
        self.topRightCol = Tkinter.Entry(self.optionFrame)
        self.topRightRow = Tkinter.Entry(self.optionFrame)
        
        botLeftL = Tkinter.Label(self.optionFrame, text="Bot left well").grid(row=3, column=0, sticky=Tkinter.W)
        self.botLeftCol = Tkinter.Entry(self.optionFrame)
        self.botLeftRow = Tkinter.Entry(self.optionFrame)
        
        botRightL = Tkinter.Label(self.optionFrame, text="Bot right well").grid(row=4, column=0, sticky=Tkinter.W)
        self.botRightCol = Tkinter.Entry(self.optionFrame)
        self.botRightRow = Tkinter.Entry(self.optionFrame)

        self.topLeftCol.grid(row=1, column=1)
        self.topLeftRow.grid(row=1, column=2)
        self.topRightCol.grid(row=2, column=1)
        self.topRightRow.grid(row=2, column=2)
        self.botLeftCol.grid(row=3, column=1)
        self.botLeftRow.grid(row=3, column=2)
        self.botRightCol.grid(row=4, column=1)
        self.botRightRow.grid(row=4, column=2)

        rootFolderButton = Tkinter.Button(self.optionFrame, text="Containing folder", command=self.selectRoot).grid(row=6, column=0)
        self.rootFolderText = Tkinter.Entry(self.optionFrame, textvariable=self.root, width=40)
        self.rootFolderText.grid(row=6,column=1, columnspan=2, sticky=Tkinter.W)

        backButton = Tkinter.Button(self.optionFrame, text="Back", command=self.inputToOptions).grid(row=7, column=0)
        submitButton = Tkinter.Button(self.optionFrame, text="Next", command=self.inputToSelect).grid(row=7, column=2)

    def getUserSelection(self):
        '''Draws the selection matrix and sets up all button events.  Each circle is in a 25x25 pixel square located in a canvas which is held in selectFrame
        Coordinates for the circles are generated in the genCoords method.
        Next and back buttons are attached to specific methods for loading and unloading frames. 
        '''
        self.canvas.bind("<ButtonPress-1>", self.startSelect)
        self.canvas.bind("<B1-Motion>", self.contSelect)
        self.canvas.bind("<Control-ButtonRelease-1>", self.stopDeselect)
        self.canvas.bind("<ButtonRelease-1>", self.stopSelect)
        for i in self.coordsy:
            for j in self.coordsx:
                circle = self.canvas.create_oval(j,i,j+25, i+25, fill='white')
                self.canvas.tag_bind(circle,'<ButtonPress-1>', self.onCircleClick)
        selectAll = Tkinter.Button(self.selectFrame, text="Select All", command=self.selectAll)
        deselectAll = Tkinter.Button(self.selectFrame, text="Deselect All", command=self.deselectAll)
        submitButton = Tkinter.Button(self.selectFrame, text="Plot", command=self.drawGraph)
        backButton = Tkinter.Button(self.selectFrame, text="Back", command=self.selectToInput)
        
        self.canvas.grid(row=0, columnspan=4)
        selectAll.grid(row=1, column=2)
        deselectAll.grid(row=1, column=1)
        submitButton.grid(row=2,column=2)
        backButton.grid(row=2,column=1)

    def optionsToInput(self):
        '''First screen to second screen.  Stores data from first screen and clears the screen and then moves to the next one.
        As all the infomation necessary for the 3rd screen is now here genCoords is called in readiness.
        '''
        self.across = float(self.wellAcross.get())
        self.down = float(self.wellDown.get())
        self.sampleTime = int(self.sampleTimeEntry.get())
        self.genCoords()
        for child in self.optionFrame.winfo_children():
            child.destroy()
        self.getUserInput()

    def inputToOptions(self):
        '''Back button for screen 2 to 1.  No data needs to be stored between here so simply clears the frame and calls the previous screen.'''
        for child in self.optionFrame.winfo_children():
            child.destroy()
        self.getUserOptions()

    def inputToSelect(self):
        '''Method to change from screen 2 to 3, stores all four vial positions as (col,row) tuples.
        When setting up the canvas for drawing the selection grid it is dynamically sized.
        '''
        self.topLeft = (int(self.topLeftCol.get()), int(self.topLeftRow.get()))
        self.topRight = (int(self.topRightCol.get()), int(self.topRightRow.get()))
        self.botLeft = (int(self.botLeftCol.get()), int(self.botLeftRow.get()))
        self.botRight = (int(self.botRightCol.get()), int(self.botRightRow.get()))
        self.optionFrame.grid_forget()
        self.selectFrame.grid()
        self.canvas.config(width=self.across*50 + 100, height=self.down*50 + 100)
        self.getUserSelection()

    def selectToInput(self):
        '''Back method from screen 3 to 2.  Clears the canvas of objects and empties the list of selected.
        Then draws screen 2.
        '''
        self.selected = []
        for obj in self.canvas.find_all():
            self.canvas.delete(obj)
            
        self.selectFrame.grid_forget()
        self.optionFrame.grid()
        self.getUserInput()

    def selectRoot(self):
        '''Callback for the containing folder button, self.root is a tkinter StringVar and is tied to the textbox adjacent to the button.'''
        self.root.set(tkFileDialog.askdirectory())

    def onCircleClick(self, event):
        '''Callback for when a circle on screen 3 is clicked.
        Toggles it's selected status with fill colour (white/red).
        Updates the selected list self.selected accordingly.
        '''
        circle = event.widget.find_closest(event.x, event.y)
        if self.canvas.itemcget(circle, 'fill') != 'white':
            self.canvas.itemconfig(circle, fill='white')
            self.selected.remove(circle[0])
        else:
            self.canvas.itemconfig(circle, fill='red')
            self.selected.append(circle[0])

    def startSelect(self, event):
        '''One of four callbacks for click and drag select functionality.
        Called on canvas click event and creates a 0 size rectangle at the current mouse position.
        Click position is then stored in self.startX/self.startY/
        '''
        self.startX = event.x
        self.startY = event.y
        if not self.selectBox:
            self.selectBox = self.canvas.create_rectangle(self.startX, self.startY, self.startX, self.startY)
            
    def contSelect(self, event):
        '''Second callback in click and drag selection.
        Called on mouse move event, the rectangle is updated so it is drawn from start to current mouse position.
        '''
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.selectBox, self.startX, self.startY, curX, curY)
    
    def stopSelect(self, event):
        '''Third callback for click and drag select, is called from a mouse button release event.
        Determines which wells are in the selection box and then checks if they are already selected.
        If not then circle is filled red and added to the selection list.
        The selection rectangle is removed from the canvas.
        '''
        selection = self.canvas.coords(self.selectBox)
        selectedWells = self.canvas.find_enclosed(selection[0], selection[1], selection[2], selection[3])
        self.canvas.delete(self.selectBox)
        self.selectBox = None
        for circle in selectedWells:
            if self.canvas.itemcget(circle, 'fill') == 'white':
                self.canvas.itemconfig(circle, fill='red')
                self.selected.append(circle)
    
    def stopDeselect(self, event):
        '''Fourth callback on click and drag selection, this is called on a mouse button release with Control pressed.
        Is the same in functionality to stopSelect but instead of selecting it deselects.
        Filling circles white and removing them from the selected list.
        '''
        selection = self.canvas.coords(self.selectBox)
        selectedWells = self.canvas.find_enclosed(selection[0], selection[1], selection[2], selection[3])
        self.canvas.delete(self.selectBox)
        self.selectBox = None
        for circle in selectedWells:
            if self.canvas.itemcget(circle, 'fill') == 'red':
                self.canvas.itemconfig(circle, fill='white')
                self.selected.remove(circle)
                
    def genCoords(self):
        '''Method to generate the coordinates to draw the circles on third screen.
        '''
        self.coordsx = [50+50*i for i in range(0,int(self.across))]
        self.coordsy = [50+50*i for i in range(0,int(self.down))]

    def genIdealGrid(self):
        '''Generates an ideal rectangle grid based off of top left and top right and bottom left.  Then infers a bottom right.
        This is then used to calculate errors between this and the actual grid
        '''
        self.iTopLeft = self.topLeft
        self.iTopRight = (self.topRight[0], self.topLeft[1])
        self.iBotLeft = (self.topLeft[0], self.botLeft[1])
        self.iBotRight = (self.topRight[0], self.botLeft[1])

    def calcSeparation(self):
        '''Calculates the spacing between wells on the ideal grid in both x and y.  Note the across -1 as there are only x-1 vials from the origin well'''
        self.xSepartation = (self.iTopRight[0] - self.iTopLeft[0]) / (self.across - 1)
        self.ySepartation = (self.iBotLeft[1] - self.iTopLeft[1]) / (self.down - 1)
        
    def calcGridErrors(self):
        '''Calculates a series of error values between the ideal grid and the actual grid.
        Makes assumptions that relative to the top left well that top right is correct in x direction and that bottom left is correct in the y direction.
        '''
        self.x1Error = self.botLeft[0] - self.iBotLeft[0]
        self.y1Error = self.topRight[1] - self.iTopRight[1]
        self.x2Error = self.botRight[0] - self.iBotRight[0]
        self.y2Error = self.botRight[1] - self.iBotRight[1]

    def calcGridSkew(self, x, y):
        '''Calcualtes a skew value for each point in x,y.  These are then added to correct for any rotational errors.
        x and y are coordinates of a well relative to the grid. For example in a 12x8 grid a well might be 9,5.  These are then used along with errors to come up with an overall offset from the ideal grid.
        '''
        xSkew = (((y/self.down) * self.x1Error) * ((self.across - x) / self.across)) + (((y / self.down) * self.x2Error) * (x / self.across))
        ySkew = (((x/self.across) * self.y1Error) * ((self.down - y) / self.down)) + (((x / self.across) * self.y2Error) * (y / self.down))
        return (xSkew, ySkew)

    def plotGrid(self):
        '''Test function to ensure that grid corrections were working correctly, just plots the coordinate values on a scatter plot'''
        plt.figure(2)
        for i in self.toPlot:
            plt.scatter(i[0], i[1])

    def translateVialToCoord(self, vials):
        '''Method that turns vial number in the grid to actual coordinates for the csv.
        Uses modular arithmatic to calculate the well's plate coordinates.
        These plate coordinates are then used along with separation and skew from origin point to calculate coordinates in the csv.
        '''
        self.toPlot = []
        self.genIdealGrid()
        self.calcGridErrors()
        self.calcSeparation()
        
        for well in vials:
            if well % self.across == 0:
                across = self.across
                down = well // self.across
            else:
                across = well % self.across
                down = well // self.across + 1
            #Ideal coordinates are 0 indexed
            across -= 1
            down -= 1
            
            skew = self.calcGridSkew(across, down)
            
            acrossCoord = self.topLeft[0] + (across * self.xSepartation) + skew[0]
            downCoord = self.topLeft[1] + (down * self.ySepartation) + skew[1]
            
            self.toPlot.append((int(acrossCoord),int(downCoord)))
        
    def selectAll(self):
        '''Callback for select all button. Adds every circle to the selected list and fills them red.'''
        for obj in self.canvas.find_all():
            if obj not in self.selected:
                self.selected.append(obj)
                self.canvas.itemconfig(obj, fill='red')
    
    def deselectAll(self):
        '''Callback for deselect all button, is inverse in functionality to selectAll'''
        for obj in self.canvas.find_all():
            if obj in self.selected:
                self.selected.remove(obj)
                self.canvas.itemconfig(obj, fill='white')        
    
    def drawGraph(self):
        '''Method to draw graph for the selected wells.  Called from the plot button on screen 3.
        Calls translateVialToCoord method and then iterates through the csv files in the root folder given.
        Each vial coordinate tuple is iterated over and data extracted and added to result.
        Result holds well data from a single csv.  Result is then added to resultList which stores data from all csvs.
        Data is then plotted with a separate line for each well.        
        '''
        self.translateVialToCoord(self.selected)
        # self.plotGrid()
        files = os.listdir(self.root.get())
        files.sort()
        resultList = []
        for f in files:
            result = []
            data = pd.read_csv(self.root.get()+"/"+f,skiprows=4, encoding='utf-16le')
            for i in self.toPlot:
                toAppend = data.at[i[1],str(i[0])]
                try:
                    float(toAppend)                    #toAppend = toAppend - 1.145701
                except Exception:
                    toAppend = float(toAppend[1:])
                    toAppend = toAppend #- 1.145701
                    #try:
                     #   float(toAppend)
                      #  toAppend= toAppend -1.145701
                    #except Exception:
                      #  toAppend = float(toAppend[1:7])
                toAppend = float(toAppend) -1.145701
                result.append(toAppend)
            resultList.append(result)
        '''Transposes result list to from lists of each csv to lists of each well.
        e.g. [[a,b,c],[d,e,f]] goes to [[a,d],[b,e],[c,f]]
        '''
        plt.figure(1)
        wellList = map(list, zip(*resultList))
        xAxis = [i*self.sampleTime for i in range(len(wellList[0]))]
        for well in wellList:
            plt.plot(xAxis, well)
        plt.ylabel("Temperature ($^\circ$C)")
        plt.xlabel("Time (secs)")
        plt.axhline(color='black')
        plt.axvline(color='black')
        plt.grid(True)
        plt.show()  
# find where temperature spikes by 2 degrees and record as nucleation event
        event = []
        events= []
        evenT = 0
        for well in wellList:
            well = str(well)
            if len(well) >6:
                well = well[2:9]

        for well in wellList:
            
            for i in range(1,len(well)):
                a=float(well[i])
                b=float(well[i-1])
                if a -1.5 >= b:
                    if b <= 2:
                        b=float(well[i-1])#-1.146
                        event.append(float(b))
#creates evenT for calculating Fraction frozen 
                    evenT = evenT +1
                    events.append(evenT)
        #print number of events to check
        print len(event) 
        event = sorted(event, key=float, reverse=True)
        # save freezing temps and well temperatures as csv
        f = open("Freezing_temps.csv", "w")
        f.write("\n".join(map(lambda x: str(x), event)))
        f.close()
        g = open("well_temps.csv", "wb")
        g.write("\n".join(map(lambda x: str(x), wellList)))
        g.close()   
        print event
       #"""asks if you want to anyalysis data and if so what type of analysis you want.
       #will save files for fraction frozen and INP per liter providing you give the right
       #info"""
        analysis = raw_input("do you want to analyises data (Y/N)")
        if analysis == "y":
            FFS_INP = raw_input("FFS or INP?")
            FFS = []
            if FFS_INP == "ffs" or FFS_INP == "FFS":#calculates fraction frozen
                for i in events:
                    a = float(i)
                    b = float(len(events))
                    ffs = a/b
                    FFS.append(ffs)
                    j = open("ffs.csv", "w")
                    j.write("\n".join(map(lambda x: str(x), FFS)))
                    j.close()
            if FFS_INP == "inp" or FFS_INP == "INP":
                SampTime =  raw_input("how long did you sample in minutes?")
                FlowRate = raw_input ("what was the flow rate in liters?")
                WashWater = raw_input("how much wash water was used in ml?")
                Nu = []
                INP = []
                for i in events:
                    a = float (i)
                    b = float (len(events))
                    nu = (b-a)/b
                    Nu.append(nu)
                for u in Nu: #calculates Nu/Na and then INP per liter
                    u = float(u)
                    S = float(SampTime)
                    F = float(FlowRate)
                    W = float(WashWater)
                    inp = -np.log(u)*((W/(0.05*(S*F))))
                    INP.append(inp)
                    ij = open("INP_perliter.csv", "w")
                    ij.write("\n".join(map(lambda x: str(x), INP)))
                    ij.close()
            if FFS_INP =="inp" or FFSS_INP == "INP":        
            #plots INP per liter
                fig, ax =  plt.subplots()
                ax.scatter(event, INP)
                plt.ylabel("INP per Liter")
                plt.xlabel("Temperature ($^\circ$C)")
                plt.axhline(color='black')
                plt.axvline(color='black')
                plt.grid(True)
                ax.set_yscale('log')
                ax.set_ylim(10**-4, 10**1)
                plt.show()  
                            
        if analysis == "n":
            print "done"


if __name__ == '__main__':
    root = Tkinter.Tk()
    app = App(root)
    root.mainloop()


