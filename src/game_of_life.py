import Tkinter as tk
from Tkinter import *

class Example(tk.Frame):
	def __init__(self, root):
		tk.Frame.__init__(self, root)

		self.menubar = tk.Menu()
		self.fileMenu = tk.Menu()
		self.menubar.add_cascade(label="File", menu=self.fileMenu)

		self.fileMenu.add_command(label="New", command=self.donothing)
		self.fileMenu.add_command(label="Open", command=self.donothing)
		self.fileMenu.add_command(label="Save", command=self.donothing)
		self.fileMenu.add_command(label="Save As", command=self.donothing)
		self.fileMenu.add_command(label="Close", command=self.donothing)

		root.configure(menu=self.menubar)

	def donothing(self):
		filewin = Toplevel(root)
		button = Button(filewin, text="Do nothing button")
		button.pack()

if __name__ == "__main__":
	root = tk.Tk()
	root.geometry("500x500")
	root.title("Game of Life")
	app = Example(root)
	app.pack(fill="both", expand=True)
	root.mainloop()