__author__ = "scrum-diddlyumptious"

from tkinter import *
import pandas as pd
import time
import csv

# Global Variables
currentRows = 50
currentColumns = 50
currentGridColor = 'black' # default grid color
storedGrid = []
storedGridIndex = 0
windowCanvasWidth = 500
windowCanvasHeight = 500
cellWidth = int(windowCanvasWidth / currentRows)
cellHeight = int(windowCanvasHeight / currentColumns)
stepNum = 0
lifeNum = 0
running = False
colors = ['black', 'blue', 'red', 'green']
tiles = [[None for _ in range(currentRows)] for _ in range(currentColumns)]
data = {'color' : '',
        'pos': []}
df = pd.DataFrame(data)
dfPrev = pd.DataFrame(data)
df2Prev = pd.DataFrame(data)

#global constants added for readability
FIRST_ITERATION = int(1)
SECOND_ITERATION = int(2)
STABILITY_CHECK_ITERATION = int(3)

waitTime = 1000 #start with 1 second slowdown of game run speed(later can multiply it by speedup/slowdown factor)

# Creates the drop down menu
def windows_menu(root,windowCanvas, e):

	# Reads the file
        def command_read_file():
                fileWin = Toplevel(root)
                button = Button(fileWin, text="Ryan will implement read file function")
                button.pack()

	# Write to file
        def command_write_file():
                fileWin = Toplevel(root)
                button = Button(fileWin, text="Ryan will implement write file function")
                button.pack()

   # Skeleton code for menu buttons actions
        def do_nothing():
                fileWin = Toplevel(root)
                button = Button(fileWin, text="Do nothing button")
                button.pack()

	# change the grid color
        def change_color(changedColors):
                global currentGridColor
                currentGridColor = changedColors

	# creates the grid line
        def create_grid(windowCanvas):
		# draw horizontal lines
                x1 = 0
                x2 = windowCanvasWidth+1
                for k in range(0, currentRows):
                        y1 = k*cellHeight
                        y2 = k*cellHeight
                        windowCanvas.create_line(x1, y1, x2, y2, tag='grid_line')

		# draw vertical lines
                y1 = 0
                y2 = windowCanvasHeight+1
                for k in range(0, currentColumns):
                        x1 = k*cellWidth
                        x2 = k*cellWidth
                        windowCanvas.create_line(x1, y1, x2, y2, tag='grid_line')

	# initialize parent menus
        menuBar = Menu(root)
        fileMenu = Menu(menuBar, tearoff=0)
        showMenu = Menu(menuBar, tearoff=0)
        actionsMenu = Menu(menuBar, tearoff=0)
        speedMenu = Menu(menuBar, tearoff=0)
        subMenuColor = Menu(menuBar, tearoff=0)

	# first drop down menu "FILE"
        menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Read File", command=lambda:load_game(root, windowCanvas))#command=command_read_file)
        fileMenu.add_command(label="Write File", command=lambda:save_game())#command=command_write_file)

	# second drop down menu "Show"
        menuBar.add_cascade(label="Show", menu=showMenu)
        showMenu.add_command(label="Static", command=do_nothing)
        showMenu.add_command(label="Oscillate", command=do_nothing)
        showMenu.add_command(label="Move", command=do_nothing)
        showMenu.add_command(label="Weird", command=do_nothing)

	# third drop down menu "Actions"
        menuBar.add_cascade(label="Actions", menu=actionsMenu)
        actionsMenu.add_command(label="Clear", command=lambda:clear_game(root, windowCanvas))#command=do_nothing)
        actionsMenu.add_command(label="Run", command=lambda:run(df, windowCanvas, root, e))
        actionsMenu.add_command(label="Step", command=lambda:refresh_life(df, windowCanvas, root))
        actionsMenu.add_command(label="Stop", command=lambda:pause_game())
        actionsMenu.add_command(label="Quit", command=root.quit)

	# fourth drop down menu "Grid/Speed"
        menuBar.add_cascade(label="Grid/Speed", menu=speedMenu)
        speedMenu.add_command(label="No Grid", command=lambda:windowCanvas.delete('grid_line'))
        speedMenu.add_command(label="Show Grid", command=lambda: create_grid(windowCanvas))
        speedMenu.add_command(label="Faster", command=lambda:change_speed(0.5)) #multiplying wait time by 0.5 decreases wait time between steps in run()
        speedMenu.add_command(label="Slower", command=lambda:change_speed(2)) #multiplying wait time by 2 doubles the wait time, giving a slower effect
        speedMenu.add_cascade(label="Color", command=do_nothing, menu=subMenuColor)

	# calling submenu color functions
        subMenuColor.add_command(label="red",command=lambda:change_color("red"))
        subMenuColor.add_command(label="blue",command=lambda:change_color("blue"))
        subMenuColor.add_command(label="green",command=lambda:change_color("green"))

	# Actually register and display the four menu dropdown menu
        root.config(menu=menuBar)

def step_counter(root):
        global stepNum
        stepNum+=1
        stepCounterLabel = Label(root, text=stepNum)
        stepCounterLabel.place(x=85, y=1)

def life_counter(root):
        global lifeNum
        global df
        lifeNum = len(df['pos'].tolist())
        lifeCounterLabel = Label(root, text=lifeNum)
        lifeCounterLabel.place(x=windowCanvasWidth-35, y=1)
def save_game():
        global df
        global dfPrev
        global df2Prev
        global lifeNum
        global stepNum
        global waitTime
        #insert input box for asking for filename
        with open('savegame.csv', mode='w', newline='') as f:
                fw = csv.writer(f,delimiter=',')
                fw.writerow([lifeNum, stepNum, waitTime])
        with open('savegame.csv', mode='a', newline='') as f:
                fw = csv.writer(f, delimiter=',')
                fw.writerow([len(df),len(dfPrev),len(df2Prev)])
                df.to_csv(f,header=False)
                dfPrev.to_csv(f,header=False)
                df2Prev.to_csv(f,header=False)
def load_game(root, windowCanvas):
        global df
        global data
        global dfPrev
        global df2Prev
        global lifeNum
        global stepNum
        global storedGridIndex
        global currentGridColor
        global waitTime
        global tiles
        global storedGrid
        global cellWidth
        global cellHeight
        clear_game(root, windowCanvas)
        with open('savegame.csv', mode='r') as f:
                fr = csv.reader(f,delimiter=',')
                row1 = next(fr)
                lifeNum = row1[0]
                stepNum = row1[1]
                waitTime = row1[2]
                row2 = next(fr)
                df = pd.read_csv('savegame.csv', skiprows=2, names=data,header=None,nrows=int(row2[0]))
                dfPrev = pd.read_csv('savegame.csv',skiprows=2+int(row2[0]), names=data, header=None, nrows=int(row2[1]))
                df2Prev = pd.read_csv('savegame.csv',skiprows=2+int(row2[0])+int(row2[1]),names=data, header=None, nrows=int(row2[2]))
                storedGridIndex = len(df)-1
                storedGrid = df['pos']
                storedGrid = [eval(x) for x in storedGrid]

                for coordinates in storedGrid:
                        tiles[coordinates[0]][coordinates[1]] = windowCanvas.create_rectangle(coordinates[0]*cellHeight, coordinates[1]*cellWidth, (coordinates[0]+1)*cellHeight, (coordinates[1]+1)*cellWidth, fill=currentGridColor,outline=currentGridColor)
        if(check_stable(df)):
                stableLabel = Label(root, text = "Stable")
                stableLabel.place(x=0, y=25)
        #need to add option to load from name and use variable in readcsv
        #need to add option to save to specific file name and error check filename in save_game
def clear_game(root, windowCanvas):
        global df
        global data
        global dfPrev
        global df2Prev
        global lifeNum
        global stepNum
        global storedGridIndex
        global currentGridColor
        global waitTime
        global tiles
        global storedGrid
        del df
        del dfPrev
        del df2Prev
        for i in range(0, len(tiles)-1):
                for x in range(0, len(tiles[0])-1):
                        if tiles[i][x] != None:
                                windowCanvas.delete(tiles[i][x])
        del storedGrid
        waitTime = 1000
        stepNum = 0
        lifeNum = 0
        storedGridIndex = 0
        df = pd.DataFrame(data)
        dfPrev = pd.DataFrame(data)
        df2Prev = pd.DataFrame(data)
        tiles = [[None for _ in range(currentRows)] for _ in range(currentColumns)]
        storedGrid = []
# Litterly copied from this website:
# https://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas
def clickable_grid(root,windowCanvas):

	# Create a grid of None to store the references to the tiles
        global df

	# Asynchronous listener
	# This is acutally the backend of the clickable grid
        def callback(event):

		# Storing and retrieving the grid length
                global storedGridIndex

		# Get rectangle diameters
                columnWidth = cellWidth
                rowHeight = cellHeight

		# Calculate column and row number
                columnNum = event.x//columnWidth
                rowNum = event.y//rowHeight
                
		# If the tile is not filled, create a rectangle
		# Also sets the grid color as well
                if not tiles[rowNum][columnNum]:
                        tiles[rowNum][columnNum] = windowCanvas.create_rectangle(columnNum*columnWidth, rowNum*rowHeight, (columnNum+1)*columnWidth, (rowNum+1)*rowHeight, fill=currentGridColor,outline=currentGridColor)
                        storedGrid.append([])
                        storedGrid[storedGridIndex].append(columnNum)
                        storedGrid[storedGridIndex].append(rowNum)
                        print('index: ',storedGridIndex)
                        df.loc[storedGridIndex] = [currentGridColor, [columnNum, rowNum]]
                        storedGridIndex+=1

		# If the tile is filled, delete the rectangle and clear the reference
                else:
                        drop = df['pos'].tolist().index([columnNum, rowNum])
                        windowCanvas.delete(tiles[rowNum][columnNum])
                        tiles[rowNum][columnNum] = None
                        del storedGrid[storedGrid.index([columnNum, rowNum])]
                        df.drop(index=drop, inplace=True)
                        storedGridIndex-=1
                        

                life_counter(root)
                print(storedGrid) # prints the coordinates on the terminal/output
                #print(df)
	# figures out how the canvas sits in the window
        windowCanvas.pack()
        windowCanvas.bind("<Button-1>", callback)
        
def run(df, windowCanvas, root, e):
        global running
        if(running == False):
                running = True
                iterationCount = int(1) #use this to know when every 3rd iteration comes bc then it is time to do a stability check
                runLoop(df, windowCanvas, root, e, iterationCount) #triggers running loop

def runLoop(df, windowCanvas, root, e, iterationCount): #added this so run function can enter an endless loop that only exits when global variable is modified
        global running
        global dfPrev
        global df2Prev
        global FIRST_ITERATION
        global SECOND_ITERATION
        global STABILITY_CHECK_ITERATION
        if(running):
                refresh_life(df, windowCanvas, root)
                if(iterationCount == FIRST_ITERATION):
                        df2Prev = df.copy() #first df to record is for 2 iterations ago
                        iterationCount += 1
                elif(iterationCount == SECOND_ITERATION):
                        dfPrev = df.copy() #now record the 'most recent' df iteration second
                        iterationCount += 1
                elif(iterationCount == STABILITY_CHECK_ITERATION):
                    #now its time to check for stability, then reset counter
                        if(check_stable(df)):
                        #(insert code here to set GUI's stable notification to visible)
                            stableLabel = Label(root, text = "Stable")
                            stableLabel.place(x=0, y=25)
                        else:
                        #(and insert code here to set GUI's stable notification to invisible)
                            stableLabel = Label(root, text = "               ")
                            stableLabel.place(x=0, y=25)
                        iterationCount = FIRST_ITERATION #reset counter
                root.update()
                root.after(waitTime, lambda:runLoop(df, windowCanvas, root, e, iterationCount)) #recursively calls itself


def check_stable(df): #takes dataframe from 2 iterations ago to compare to the current frame
    global df2Prev
    return df.equals(df2Prev)

def pause_game():
    global running
    running = False
    
def change_speed(factor): #factor = 2 to slow down, 0.5 to speedup
    global waitTime
    if(factor > 1):
        waitTime *= factor
    elif (factor > 0 and factor < 1):
        dividend = 1 / factor #converting fraction to an integer to divide by bc tkinter.after requires int
        dividend = int(dividend)
        result = waitTime / dividend #waitTime must stay int at all times, since we are working with threads
        waitTime = int(result)
        
#refesh life function
#takes in the pandas dataframe as a parameter and determines whether the cells on the grid live or die
def refresh_life(df, windowCanvas, root):
        nextGrid = []
        
        global storedGrid
        col = []
        step_counter(root)

        
        
        #loop over all the cells in the grid
        for i in range(0, currentColumns):
                for j in range(0, currentRows):
                        cellColor = 'white'
                        
                        index = {
                                'left':currentColumns-1 if (i-1)<0 else i-1, #left
                                'right':(i+1)%currentColumns,                #right
                                'up':currentRows-1 if (j-1)<0 else j-1,        #up
                                'down':(j+1)%currentRows                     #down
                        }
                        #count the number of neighbors for the cell
                        neighborList = [
                                1 if [index['left'], index['up']] in df['pos'].tolist() else 0,   #top left
                                1 if [i, index['up']] in storedGrid else 0,            #top mid
                                1 if [index['right'], index['up']] in df['pos'].tolist() else 0,  #top right
                                1 if [index['right'], j] in storedGrid else 0,         #mid right
                                1 if [index['right'], index['down']] in df['pos'].tolist() else 0,#bottom right
                                1 if [i, index['down']] in storedGrid else 0,          #mid bottom
                                1 if [index['left'], index['down']] in df['pos'].tolist() else 0, #bottom left
                                1 if [index['left'], j] in storedGrid else 0           #mid left
                        ]

                        numNeighbors = sum(neighborList)
                        
                        #Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                        #if [i, j] in df.pos and numNeighbors < 2:
                                #do nothing
                        #Any live cell with two or three live neighbours lives on to the next generation.
                        if [i, j] in df['pos'].tolist() and (numNeighbors == 2 or numNeighbors == 3):
                                nextGrid.append([i,j])
                                print(df['pos'].tolist().index([i,j]))
                                col.append(df['color'].tolist()[df['pos'].tolist().index([i,j])])
                        #Any live cell with more than three live neighbours dies, as if by overpopulation.
                        #if [i, j] in df.pos and numNeighbors < 2:
                        #Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                        if [i, j] not in df['pos'].tolist() and numNeighbors == 3:
                                nextGrid.append([i, j])
                                
                                if [index['left'], index['up']] in df['pos'].tolist():
                                        currentGridColor = (df['color'].tolist()[df['pos'].tolist().index([index['left'],index['up']])])
                                        col.append(df['color'].tolist()[df['pos'].tolist().index([index['left'],index['up']])])
                                elif [i, index['up']] in df['pos'].tolist():            #top mid
                                        currentGridColor = (df['color'].tolist()[df['pos'].tolist().index([i,index['up']])])
                                        col.append(df['color'].tolist()[df['pos'].tolist().index([i,index['up']])])
                                elif [index['right'], index['up']] in df['pos'].tolist():  #top right
                                        currentGridColor = (df['color'].tolist()[df['pos'].tolist().index([index['right'],index['up']])])
                                        col.append(df['color'].tolist()[df['pos'].tolist().index([index['right'],index['up']])])
                                elif [index['right'], j] in df['pos'].tolist():         #mid right
                                        currentGridColor = (df['color'].tolist()[df['pos'].tolist().index([index['right'],j])])
                                        col.append(df['color'].tolist()[df['pos'].tolist().index([index['right'],j])])
                                elif [index['right'], index['down']] in df['pos'].tolist(): #bottom right
                                        currentGridColor = (df['color'].tolist()[df['pos'].tolist().index([index['right'],index['down']])])
                                        col.append(df['color'].tolist()[df['pos'].tolist().index([index['right'],index['down']])])
                                elif [i, index['down']] in df['pos'].tolist():          #mid bottom
                                        currentGridColor = (df['color'].tolist()[df['pos'].tolist().index([i,index['down']])])
                                        col.append(df['color'].tolist()[df['pos'].tolist().index([i,index['down']])])
                                elif [index['left'], index['down']] in df['pos'].tolist(): #bottom left
                                        currentGridColor = (df['color'].tolist()[df['pos'].tolist().index([index['left'],index['down']])])
                                        col.append(df['color'].tolist()[df['pos'].tolist().index([index['left'],index['down']])])
                                elif [index['left'], j] in df['pos']:           #mid left
                                        currentGridColor = (df['color'].tolist()[df['pos'].tolist().index([index['left'],j])])
                                        col.append(df['color'].tolist()[df['pos'].tolist().index([index['left'],j])])
                                else:
                                        currentGridColor = ('white')

        global storedGridIndex
        del storedGrid[:]
        
        
        storedGrid = nextGrid[:]
        
        df.drop(df.index[0:storedGridIndex], inplace=True)
        storedGridIndex = len(nextGrid)
        print('new dataframe:')
        print(df)
        #df['pos'] = nextGrid
        #df['color'] = col
        for i in range(0, storedGridIndex):
                df.loc[i] = [col[i], nextGrid[i]]

        
        for i in range(0, currentColumns):
                for j in range(0, currentRows):
                        # Get rectangle diameters
                        columnWidth = cellWidth
                        rowHeight = cellHeight
                        
	                # Calculate column and row number
                        columnNum = i
                        rowNum = j
                        currentGridColor = 'white' if [i,j] not in df['pos'].tolist() else df['color'].tolist()[df['pos'].tolist().index([i,j])]
                                        
		        # If the tile is not filled, create a rectangle
		        # Also sets the grid color as well
                        if not tiles[rowNum][columnNum] and [i,j] in nextGrid:
                                tiles[rowNum][columnNum] = windowCanvas.create_rectangle(columnNum*columnWidth, rowNum*rowHeight, (columnNum+1)*columnWidth, (rowNum+1)*rowHeight, fill=currentGridColor,outline = currentGridColor)

		                # If the tile is filled, delete the rectangle and clear the reference
                        if (tiles[rowNum][columnNum] != None and [i,j] not in nextGrid):
                                windowCanvas.delete(tiles[rowNum][columnNum])
                                tiles[rowNum][columnNum] = None
                                
        life_counter(root)

# Main function
def main():

	# class alias to variable
        root = Tk()
	# title of the program
        root.title("Game of Life")
        e = Entry(root)
	# initialize window size and color
        windowCanvas = Canvas(root, width=windowCanvasWidth, height=windowCanvasHeight, borderwidth=0, background='white', highlightbackground = 'black')    

	# create instructions
        Label(root, text="Instructions:\nChoose From Dropdown Menu Or Left Click Grid Points \n Right click to run one step").pack()

	#Displaying step counter
        Label(root, text="Step Count: ").place(x=0, y=1)

	#Displaying life counter
        Label(root, text="Life Count: ").place(x=windowCanvasWidth-120, y=1)

	# backend grid listener
        clickable_grid(root,windowCanvas)

	# creates the menu
        windows_menu(root,windowCanvas, e)

	# the pack geometry manager organises widgets in horizontal and vertical boxes
        windowCanvas.pack()

	# start monitoring and updating the GUI.
        root.mainloop()


# Calls main function
if __name__== "__main__":
        main()
