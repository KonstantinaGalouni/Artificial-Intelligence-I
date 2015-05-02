#!/usr/bin/env python
#!/usr/bin/python

"""AlienTiles Problem"""

from search import *
import sys

from Tkinter import Tk, Text, BOTH, W, N, E, S
import Tkinter as tk
import tkMessageBox
from ttk import Frame, Button, Label, Style

#dic = { 'goal' : int(sys.argv[2])}
#dimension = int(sys.argv[1])  #dimension of the table

dic = {'goal' : 0}
dimension = 3

class AlienTilesProblem(Problem) :
	"""Subclass of search.Problem"""

	def __init__(self, n) :
		"""input n: size of table """

#---------------------------Helpful variables
		red = 0
		green = 0
		blue = 0
		purple = 0
#---------------------------

		# Readind from file
		f = open('myinput.txt', 'r')

		print("Filename is:"+f.name)

		#Reading line-to-line
		count = 0
		allwords = []
		for line in f:
		# The function split is useful in order to make parse a file
			word = line.split(" ")
			for w in range(len(word)):
				allwords.insert(count+w, word[w])
				#helpfl variables----------------------------------
				if int(allwords[len(allwords) - 1]) == 0 :
					red = red + 1
				elif int(allwords[len(allwords) - 1]) == 1 :
					green = green + 1
				elif int(allwords[len(allwords) - 1]) == 2 :
					blue = blue + 1
				elif int(allwords[len(allwords) - 1]) == 3 :
					purple = purple + 1
				#---------------------------------------------------
			count += len(word)
		count = len(allwords)

		f.close()

		t1 = [int(allwords[i]) for i in range(count)]

		t2 = (tuple(t1), red, green, blue, purple)
        
		super(AlienTilesProblem, self).__init__(tuple(t2), None)
		self.n = n

        
	def actions(self, state) :
		return [ (l, c) for l in range(self.n) for c in range(self.n)]


	def result(self, state, action) :
		l = action[0]	#line
		c = action[1]	#column

		# Copy state
		newStateList = list(state)
		newStateList[0] = list(state[0])

		#position of each tile is described as (line*dimension + column)

		for i in range(self.n):
			if i != c :		#all tiles in this column change
				newStateList[0][l*self.n + i] = (newStateList[0][l*self.n + i] + 1) % 4
                
				#helpful variables------------------------
				if newStateList[0][l*self.n + i] == 0 :
					newStateList[1] += 1	#red = red + 1
					newStateList[4] -= 1	#purple = purple - 1
				elif newStateList[0][l*self.n + i] == 1 :
					newStateList[2] += 1	#green = green + 1
					newStateList[1] -= 1	#red = red - 1
				elif newStateList[0][l*self.n + i] == 2 :
					newStateList[3] += 1	#blue = blue + 1
					newStateList[2] -= 1	#green = green - 1
				elif newStateList[0][l*self.n + i] == 3 :
					newStateList[4] += 1	#purple = purple + 1
					newStateList[3] -= 1	#blue = blue - 1

			if i != l :		#all tiles in this line change
				newStateList[0][i*self.n + c] = (newStateList[0][i*self.n + c] + 1) % 4

				if newStateList[0][i*self.n + c] == 0 :
					newStateList[1] += 1	#red = red + 1
					newStateList[4] -= 1	#purple = purple - 1
				elif newStateList[0][i*self.n + c] == 1 :
					newStateList[2] += 1	#green = green + 1
					newStateList[1] -= 1	#red = red - 1
				elif newStateList[0][i*self.n + c] == 2 :
					newStateList[3] += 1	#blue = blue + 1
					newStateList[2] -= 1	#green = green - 1
				elif newStateList[0][i*self.n + c] == 3 :
					newStateList[4] += 1	#purple = purple + 1
					newStateList[3] -= 1	#blue = blue - 1

		#change the chosen tile
		newStateList[0][l*self.n + c] = (newStateList[0][l*self.n + c] + 1) % 4

		#helpful variables------------------------
		if newStateList[0][l*self.n + c] == 0 :
			newStateList[1] += 1	#red = red + 1
			newStateList[4] -= 1	#purple = purple - 1
		elif newStateList[0][l*self.n + c] == 1 :
			newStateList[2] += 1	#green = green + 1
			newStateList[1] -= 1	#red = red - 1
		elif newStateList[0][l*self.n + c] == 2 :
			newStateList[3] += 1	#blue = blue + 1
			newStateList[2] -= 1	#green = green - 1
		elif newStateList[0][l*self.n + c] == 3 :
			newStateList[4] += 1	#purple = purple + 1
			newStateList[3] -= 1	#blue = blue - 1
		#-------------------------------------------

		temp_t = (tuple(newStateList[0]), newStateList[1], newStateList[2], newStateList[3], newStateList[4])
		return(temp_t)


	def goal_test(self, state) :
		goal = dic['goal']

		#state[goal + 1] is the colour we set as goal
		if state[goal + 1] == self.n*self.n :
			return True
		else :
			return False

               
#-------------h functions-----------

def h1(n) :
	goal = dic['goal']
	state = n.state
	if state[goal + 1] == 4 :
		return 0
	else :
		return 1


def h2(n) :
	state = n.state
	#all the tiles should have "goal" colour in the end
	goal = dic['goal']
	distance = 0            #largest distance between farest(from goal) colour in the table 
	number = 0              #how many tiles have the farest(from goal) colour in the table

	if goal == 0 :              #goal = red
		if state[2] != 0 :      #green
			distance = 3
			number = state[2]
		elif state[3] != 0 :    #blue
			distance = 2
			number = state[3]
		elif state[4] != 0 :	#purple
			distance = 1
			number = state[4]
	elif goal == 1 :         	#goal = green
		if state[3] != 0 :      #blue
			distance = 3
			number = state[3]
		elif state[4] != 0 :   	#purple
			distance = 2
			number = state[4]
		elif state[1] != 0 :    #red
			distance = 1
			number = state[1]
	elif goal == 2 :         	#goal = blue
		if state[4] != 0 :      #purple
			distance = 3
			number = state[4]
		elif state[1] != 0 :    #red
			distance = 2
			number = state[1]
		elif state[2] != 0 :    #green
			distance = 1
			number = state[2]
	elif goal == 3 :         	#goal = purple
		if state[1] != 0 :      #red
			distance = 3
			number = state[1]
		elif state[2] != 0 :    #green
			distance = 2
			number = state[2]
		elif state[3] != 0 :	#blue
			distance = 1
			number = state[3]

#	if number >= (2*dimension - 1) :  #2*dimension - 1 tiles should change in the last move
#		return ((number / (2*dimension - 1)) * distance)
#	else :
#		return distance

	if number >= (2*dimension - 1) :  #2*dimension - 1 tiles should change in the last move
		if (number % (2*dimension - 1)) == 0:
			return ((number / (2*dimension - 1)) * distance)
		else :
			return (((number / (2*dimension - 1)) * distance) + distance)
	else :
		return distance


def h3(n) :
	state = n.state
	#all the tiles should have "goal" colour in the end
	goal = dic['goal']
	distance = 0            #largest distance between farest(from goal) colour in the table 
	number = 0              #how many tiles have the farest(from goal) colour in the table

	if goal == 0 :              #goal = red
		if state[2] != 0 :      #green
			distance = 3
			number = state[2]
		elif state[3] != 0 :    #blue
			distance = 2
			number = state[3]
		elif state[4] != 0 :	#purple
			distance = 1
			number = state[4]
	elif goal == 1 :         	#goal = green
		if state[3] != 0 :      #blue
			distance = 3
			number = state[3]
		elif state[4] != 0 :   	#purple
			distance = 2
			number = state[4]
		elif state[1] != 0 :    #red
			distance = 1
			number = state[1]
	elif goal == 2 :         	#goal = blue
		if state[4] != 0 :      #purple
			distance = 3
			number = state[4]
		elif state[1] != 0 :    #red
			distance = 2
			number = state[1]
		elif state[2] != 0 :    #green
			distance = 1
			number = state[2]
	elif goal == 3 :         	#goal = purple
		if state[1] != 0 :      #red
			distance = 3
			number = state[1]
		elif state[2] != 0 :    #green
			distance = 2
			number = state[2]
		elif state[3] != 0 :	#blue
			distance = 1
			number = state[3]

#+++++++++Symmetry++++++++

	c = 0
#	if n.parent != None:
#		i=0
#		j=0
#		while i<=dimension-1 and j<=dimension-1 :
#			if state[0][i*dimension+j] != state[0][j*dimension+1] :
#				c=0.5
#				break
#			else:
#				i+=1
#				if i< dimension-1:
#					j+=1
#				else:
#					j=i
#			for a in p.actions(state) :
#				if p.result(n.parent.state, a) == state:
#					if a[0]>a[1] :
#						c=0
#						break

#+++++++++++++++++++++++++

#cheat variable is useful only if we create something to take advantage of the symmetries
	if distance == 0 :
		return 0	#goal state
	if number == 2*dimension - 1 :
		return distance - c
	elif number > (2*dimension - 1) :  #2*dimension - 1 tiles should change in the last move
		if (number % (2*dimension - 1)) == 0 :
			return (((number / (2*dimension - 1)) * distance) - c)
		else :
			return (((number / (2*dimension - 1)) * distance) + distance - c)
	else :
		if number + state[goal + 1] == dimension*dimension :
			return 4
		else :
			return distance - c



#=========================================
#Code like main in c/c++

p = AlienTilesProblem(dimension)                              
##print "Initial state : "
##print p.initial[0]
##print "red = {}  green = {}  blue = {}  purple = {}".format(p.initial[1], p.initial[2], p.initial[3], p.initial[4])
##print
##
###for a in p.actions(p.initial) :
###    print "l = {}, c = {}".format(a[0], a[1])
###    temp = p.result(p.initial, a)
###    print temp[0]
###    print "red = {}  green = {}  blue = {}  purple = {}".format(temp[1], temp[2], temp[3], temp[4])
##
##solution = astar_search(p, lambda node : h2(node))
##
##l = list([solution.state])
##
##for r in l :
##	l1 = list(r)
##	print "solution state"
##	print l1[0]
##	print "red = {}, green = {}, blue = {}, purple = {}".format(l1[1], l1[2], l1[3], l1[4])


###=========================GUI=========================

btn = []

class AlienTilesGui(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)   
         
		self.parent = parent
        
		self.initUI()
        
	def initUI(self):      
		self.parent.title("AlienTiles")
		self.style = Style()
		self.style.theme_use("default")
		self.pack(fill=BOTH, expand=1)
        
		lbl = Label(self, text="Choose goal colour:")
		lbl.grid(sticky=W, padx=5, columnspan=4)

		redbtn = tk.Button(self, width=3, command = self.colour_red, bg='red')
		redbtn.grid(row=1, column=0, padx=12, pady=10)

		greenbtn = tk.Button(self, width=3, command = self.colour_green, bg='green')
		greenbtn.grid(row=1, column=1, padx=12, pady=10)

		bluebtn = tk.Button(self, width=3, command = self.colour_blue, bg='blue')
		bluebtn.grid(row=1, column=2, padx=12, pady=10)

		purplebtn = tk.Button(self, width=3, command = self.colour_purple, bg='purple')
		purplebtn.grid(row=1, column=3, padx=12, pady=10)
        
		for i in range(dimension) :
			for j in range(dimension) :
				btn.insert(i*dimension+j, tk.Button(self, width=5, bg='red'))
				btn[i*dimension+j].grid(row=i+2, column=j, padx=10, pady=1)
        
		hbtn = Button(self, text="Help", command = self.print_help)
		hbtn.grid(row=dimension+3, column=0, padx=1)

		ibtn = Button(self, text="Initial State", command = self.initial_state)
		ibtn.grid(row=dimension+3, column=1, padx=1)

		sbtn = Button(self, text="Solution", command = self.solution)
		sbtn.grid(row=dimension+3, column=2, padx=1)        

	def colour_red(self) :
		dic['goal'] = 0

	def colour_green(self) :
		dic['goal'] = 1

	def colour_blue(self) :
		dic['goal'] = 2

	def colour_purple(self) :
		dic['goal'] = 3

	def initial_state(self) :
		list_temp = list(p.initial[0])
		for i in range(dimension) :
			for j in range(dimension) :
				if list_temp[i*dimension+j] == 0 :
					tk.Button.configure(btn[i*dimension+j], bg = "red")
				elif list_temp[i*dimension+j] == 1 :
					tk.Button.configure(btn[i*dimension+j], bg = "green")
				elif list_temp[i*dimension+j] == 2 :
					tk.Button.configure(btn[i*dimension+j], bg = "blue")
				elif list_temp[i*dimension+j] == 3 :
					tk.Button.configure(btn[i*dimension+j], bg = "purple")

	def solution(self) :
		solution = astar_search(p, lambda node : h3(node))

		l = list([solution.state])

		for r in l :
			l1 = list(r)
			l2 = list(l1[0])
			for i in range(dimension) :
				for j in range(dimension) :
					if l2[i*dimension+j] == 0 :
						tk.Button.configure(btn[i*dimension+j], bg = "red")
					elif l2[i*dimension+j] == 1 :
						tk.Button.configure(btn[i*dimension+j], bg = "green")
					elif l2[i*dimension+j] == 2 :
						tk.Button.configure(btn[i*dimension+j], bg = "blue")
					elif l2[i*dimension+j] == 3 :
						tk.Button.configure(btn[i*dimension+j], bg = "purple")

	def print_help(self) :
		tkMessageBox.showinfo( "Helpful Directions", "First choose the goal colour by clicking one of the colourful buttons on the top\nIf you press the button 'initial state', buttons will turn to the colour of the input file\n If you press the button 'solution' the A* algorithm will give you the solution for this initial state ")

def main():
  
	root = Tk()
	root.geometry("300x250+250+250")
	app = AlienTilesGui(root)
	root.mainloop()  


if __name__ == '__main__':
	main()  

##
###=====================end of gui======================
