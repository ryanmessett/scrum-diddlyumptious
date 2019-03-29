__author__ = "scrum-diddlyumptious"

from Tkinter import *

#global variable for changing colors
color = 'black'

#Creates the menu 
def windows_menu(root):
  
    #Reads the file
    def command_read_file():
       filewin = Toplevel(root)
       button = Button(filewin, text="Ryan will implement read file function")
       button.pack()

    #Write to file
    def command_write_file():
       filewin = Toplevel(root)
       button = Button(filewin, text="Ryan will implement write file function")
       button.pack()

  #Skeleton code for menu buttons actions
    def sub_menu_color():
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

   #Skeleton code for menu buttons actions
    def do_nothing():
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    #change the grid color to red
    def add_red_color():
        global color
        color="red"

    #change the grid color to blue
    def add_blue_color():
        global color
        color="blue"

    #change the grid color to green
    def add_green_color():
        global color
        color="green"

    #initialize parent menus
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    showMenu = Menu(menubar, tearoff=0)
    actionsMenu = Menu(menubar, tearoff=0)
    speedMenu = Menu(menubar, tearoff=0)
    sub_menu_color = Menu(menubar, tearoff=0)

    #first drop down menu "FILE"
    menubar.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Read File", command=command_read_file)
    filemenu.add_command(label="Write File", command=command_write_file)

    #second drop down menu "Show"
    menubar.add_cascade(label="Show", menu=showMenu)
    showMenu.add_command(label="Static", command=do_nothing)
    showMenu.add_command(label="Oscillate", command=do_nothing)
    showMenu.add_command(label="Move", command=do_nothing)
    showMenu.add_command(label="Weird", command=do_nothing)

    #third drop down menu "Actions"
    menubar.add_cascade(label="Actions", menu=actionsMenu)
    actionsMenu.add_command(label="Clear", command=do_nothing)
    actionsMenu.add_command(label="Run", command=do_nothing)
    actionsMenu.add_command(label="Stop", command=do_nothing)
    actionsMenu.add_command(label="Quit", command=root.quit)

    #fourth drop down menu "Grid/Speed"
    menubar.add_cascade(label="Grid/Speed", menu=speedMenu)
    speedMenu.add_command(label="No Grid", command=do_nothing)
    speedMenu.add_command(label="Show Grid", command=do_nothing)
    speedMenu.add_command(label="Faster", command=do_nothing)
    speedMenu.add_command(label="Slower", command=do_nothing)
    speedMenu.add_cascade(label="Color", command=do_nothing, menu=sub_menu_color)

    #calling submenu color functions
    sub_menu_color.add_command(label="red",command=add_red_color)
    sub_menu_color.add_command(label="blue",command=add_blue_color)
    sub_menu_color.add_command(label="green",command=add_green_color)

    #Actually register and display the four menu dropdown menu
    root.config(menu=menubar)


#Litterly copied from this website:
#https://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas
def windows_grid(windowCanvas):

    # Set number of rows and columns
    ROWS = 5
    COLS = 5

    # Create a grid of None to store the references to the tiles
    tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]

    #Asynchronous listener
    def callback(event):

        # Get rectangle diameters
        col_width = windowCanvas.winfo_width()/COLS
        row_height = windowCanvas.winfo_height()/ROWS

        # Calculate column and row number
        col = event.x//col_width
        row = event.y//row_height

        # If the tile is not filled, create a rectangle
        # Also determines the grid color as well
        if not tiles[row][col]:
            tiles[row][col] = windowCanvas.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=color)
        
        # If the tile is filled, delete the rectangle and clear the reference
        else:
            windowCanvas.delete(tiles[row][col])
            tiles[row][col] = None

    # figures out how the canvas sits in the window
    windowCanvas.pack()
    windowCanvas.bind("<Button-1>", callback)


#Main function
def main():
    #class alias to variable
    root = Tk()

    #title of the program
    root.title("Game of Life")

    #initialize window size and color
    windowCanvas = Canvas(root, width=500, height=500, borderwidth=5, background='white')

    #create instructions
    Label(root, text="Instructions: \n  CHOOSE FROM DROPDOWN MENU OR RIGHT CLICK GRID POINTS \n Left click to run one step").pack()
    
    #creates the grid
    windows_grid(windowCanvas)

    #creates the menu
    windows_menu(root)

    #start monitoring and updating the GUI.
    root.mainloop()


#Calls main function
if __name__== "__main__":
    main()
