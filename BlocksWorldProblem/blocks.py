"""Blocks World Problem"""

from search import *
import sys

#dimension = int(sys.argv[1])

dimension = 5

class BlockWorldProblem(Problem) :
        """Subclass of search.Problem"""

        def __init__(self, n) :
                """input n: size of table """

                # Readind from file
                f = open('myblocks.txt', 'r')

                print("Filename is:"+f.name)

                #Reading line-to-line
                count = 0
                lines = 0
                allblocks = []
                for line in f:
                        # The function split is useful in order to make parse a file
                        word = line.split(" ")
                        allblocks.insert(count, word)
                        count += len(word)
                        lines += 1

                count = len(allblocks)

                f.close()

                t1 = [(int(allblocks[i][0]), int(allblocks[i][1])) for i in range(lines)]
        
                super(BlockWorldProblem, self).__init__(tuple(t1), None)
                self.n = n

        def actions(self, state) :
                l1 = []
                for i in range(self.n) :
                    if state[i][1] == -1 :
                        l1.insert(self.n, i)
                    else :
                        continue
                l2 = list(l1)
                l2.insert(self.n+1, -1)
                return [ (i,j) for i in l1 for j in l2 if i!=j and state[i][0] != j ]

        def result(self, state, action) :
                moving = action[0]  #this block is free and we will move it
                chosen = action[1]  #this block (or table) is free and "moving" block will be placed on it

                # Copy state
                newStateList = list(state)
                newStateList[moving] = list(state[moving])
                old_block = newStateList[moving][0]
                if old_block != -1 :
                        newStateList[old_block] = list(state[old_block]) 
                        newStateList[old_block][1] = -1
                        newStateList[old_block] = tuple(newStateList[old_block])
                newStateList[moving] = list(state[moving])
                newStateList[moving][0] = chosen
                newStateList[moving] = tuple(newStateList[moving])

                if chosen != -1 :
                        newStateList[chosen] = list(state[chosen])
                        newStateList[chosen][1] = moving
                        newStateList[chosen] = tuple(newStateList[chosen])

                return tuple(newStateList)

        def goal_test(self, state) :
                f = open('mygoalblocks.txt', 'r')

                #Reading line-to-line
                count = 0
                lines = 0
                allblocks = []
                for line in f:
                  # The function split is useful in order to make parse a file
                    word = line.split(" ")
                    allblocks.insert(count, word)
                    count += len(word)
                    lines += 1

                count = len(allblocks)

                f.close()

                l1 = [(int(allblocks[i][0]), int(allblocks[i][1])) for i in range(lines)]

                same = 0

                for i in range(self.n) :
                        if l1[i][0] == state[i][0] and l1[i][1] == state[i][1] :
                                same += 1
                if same == self.n :
                        return True
                else :
                        return False
                
###-------------h functions-----------

def h1(n) :
        state = n.state
        
        f = open('mygoalblocks.txt', 'r')

        #Reading line-to-line
        count = 0
        lines = 0
        allblocks = []
        for line in f:
                # The function split is useful in order to make parse a file
                word = line.split(" ")
                allblocks.insert(count, word)
                count += len(word)
                lines += 1

        count = len(allblocks)

        f.close()

        l1 = [(int(allblocks[i][0]), int(allblocks[i][1])) for i in range(lines)]

        position_ok = 0

        for i in range(dimension) :
                if l1[i][0] == state[i][0] :
                        position_ok += 1
        if position_ok == dimension :
                return 0        #if goal state
        else :
                return 1        #any other state different from goal

def h2(n) :
        state = n.state
        
        f = open('mygoalblocks.txt', 'r')

        #Reading line-to-line
        count = 0
        lines = 0
        allblocks = []
        for line in f:
                # The function split is useful in order to make parse a file
                word = line.split(" ")
                allblocks.insert(count, word)
                count += len(word)
                lines += 1

        count = len(allblocks)

        f.close()

        l1 = [(int(allblocks[i][0]), int(allblocks[i][1])) for i in range(lines)]

        position_ok = 0

        for i in range(dimension) :
                if l1[i][0] == state[i][0] :
                        position_ok += 1
        return dimension - position_ok  #number of blocks in wrong position

def h3(n) :
        state = n.state
        
        f = open('mygoalblocks.txt', 'r')

        #Reading line-to-line
        count = 0
        lines = 0
        allblocks = []
        for line in f:
                # The function split is useful in order to make parse a file
                word = line.split(" ")
                allblocks.insert(count, word)
                count += len(word)
                lines += 1

        count = len(allblocks)

        f.close()

        l1 = [(int(allblocks[i][0]), int(allblocks[i][1])) for i in range(lines)]

#----------------------circle for two----------------------------
#        for i in range(dimension) :     #for every block
#                if l1[i][0] != state[i][0]:
#                        if l1[state[l1[i][0]][0]][0] == state[l1[i][0]][1] :
#                                break
#        return 3
#----------------------------------------------------------------

        wrong_position = 0
        top = 0

        for i in range(dimension) :
                if l1[i][0] != state[i][0] :
                        wrong_position += 1
                        stop = 0
                        above = i
                        while stop==0 :
                                if l1[above][1] != state[above][1] :
                                        stop = 1
                                else :
                                        above = l1[above][1]
                                        top = top + 1
        return wrong_position + 2*top

#=========================================
#Code like main in c/c++

p = BlockWorldProblem(dimension)
print "Initial State is {}".format(p.initial)

#if p.goal_test(p.initial) == True :
#        print "Success"
#else :
#        print "Failure"

#for a in p.actions(p.initial) :
#	print "Returned action = {}".format(a)
#	print p.result(p.initial, a)
#	if p.goal_test(p.result(p.initial, a)) == True :
#		print "Success with the above action"
#	else :
#		print "Failure with the above action"

solution = astar_search(p, lambda node : h3(node))

print "solution state"
print solution
