__author__ = "scrum-diddlyumptious"

from Tkinter import *

# Global Variables
currentRows = 10
currentColumns = 10
currentGridColor = 'black' # default grid color
storedGrid = []
storedGridIndex = 0


# Creates the drop down menu 
def windows_menu(root,windowCanvas):

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
		x2 = currentRows*50
		for k in range(0, currentRows*50, 52):
			y1 = k
			y2 = k
			windowCanvas.create_line(x1, y1, x2, y2, tag='grid_line')

		# draw vertical lines
		y1 = 0
		y2 = currentColumns*50
		for k in range(0, currentColumns*50, 52):
			x1 = k
			x2 = k
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
	fileMenu.add_command(label="Read File", command=command_read_file)
	fileMenu.add_command(label="Write File", command=command_write_file)

	# second drop down menu "Show"
	menuBar.add_cascade(label="Show", menu=showMenu)
	showMenu.add_command(label="Static", command=do_nothing)
	showMenu.add_command(label="Oscillate", command=do_nothing)
	showMenu.add_command(label="Move", command=do_nothing)
	showMenu.add_command(label="Weird", command=do_nothing)

	# third drop down menu "Actions"
	menuBar.add_cascade(label="Actions", menu=actionsMenu)
	actionsMenu.add_command(label="Clear", command=do_nothing)
	actionsMenu.add_command(label="Run", command=do_nothing)
	actionsMenu.add_command(label="Step", command=do_nothing)
	actionsMenu.add_command(label="Stop", command=do_nothing)
	actionsMenu.add_command(label="Quit", command=root.quit)

	# fourth drop down menu "Grid/Speed"
	menuBar.add_cascade(label="Grid/Speed", menu=speedMenu)
	speedMenu.add_command(label="No Grid", command=lambda:windowCanvas.delete('grid_line'))
	speedMenu.add_command(label="Show Grid", command=lambda: create_grid(windowCanvas))
	speedMenu.add_command(label="Faster", command=do_nothing)
	speedMenu.add_command(label="Slower", command=do_nothing)
	speedMenu.add_cascade(label="Color", command=do_nothing, menu=subMenuColor)

	# calling submenu color functions
	subMenuColor.add_command(label="red",command=lambda:change_color("red"))
	subMenuColor.add_command(label="blue",command=lambda:change_color("blue"))
	subMenuColor.add_command(label="green",command=lambda:change_color("green"))

	# Actually register and display the four menu dropdown menu
	root.config(menu=menuBar)


# Litterly copied from this website:
# https://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas
def clickable_grid(root,windowCanvas):

	# Create a grid of None to store the references to the tiles
	tiles = [[None for _ in range(currentColumns)] for _ in range(currentRows)]

	# Asynchronous listener
	# This is acutally the backend of the clickable grid
	def callback(event):

		# Storing and retrieving the grid length
		global storedGridIndex

		# Get rectangle diameters
		columnWidth = (windowCanvas.winfo_width())/currentColumns
		rowHeight = (windowCanvas.winfo_height())/currentRows

		# Calculate column and row number
		columnNum = event.x//columnWidth
		rowNum = event.y//rowHeight

		# stores the x,y clicked coordinates to 2d array
		# useful for debugging for the other backend implementations
		storedGrid.append([])
		storedGrid[storedGridIndex].append(rowNum)
		storedGrid[storedGridIndex].append(columnNum)
		print(storedGrid) # prints the coordinates on the terminal/output
		storedGridIndex+=1

		# If the tile is not filled, create a rectangle
		# Also sets the grid color as well
		if not tiles[rowNum][columnNum]:
			tiles[rowNum][columnNum] = windowCanvas.create_rectangle(columnNum*columnWidth, rowNum*rowHeight, (columnNum+1)*columnWidth, (rowNum+1)*rowHeight, fill=currentGridColor,outline='white')

		# If the tile is filled, delete the rectangle and clear the reference
		else:
			windowCanvas.delete(tiles[rowNum][columnNum])
			tiles[rowNum][columnNum] = None

	# figures out how the canvas sits in the window
	windowCanvas.pack()
	windowCanvas.bind("<Button-1>", callback)


# Main function
def main():

	# class alias to variable
	root = Tk()

	# title of the program
	root.title("Game of Life")

	# initialize window size and color
	windowCanvas = Canvas(root, width=currentRows*50, height=currentColumns*50, borderwidth=currentRows, background='white')    

	# create instructions
	Label(root, text="Instructions:\nChoose From Dropdown Menu Or Right Click Grid Points \n Left click to run one step").pack()

	# backend grid listener
	clickable_grid(root,windowCanvas)

	# creates the menu
	windows_menu(root,windowCanvas)

	# the pack geometry manager organises widgets in horizontal and vertical boxes
	windowCanvas.pack()

	# start monitoring and updating the GUI.
	root.mainloop()


# Calls main function
if __name__== "__main__":
	main()
