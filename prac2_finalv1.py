# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 18:04:05 2018

@author: Vishal Thalla(16053525)
"""
"""
TODO:
    adapt Node class for this practical
    create Uniform cost function:**DONE**
    create Greedy Best search:**DONE**
    create A* search: **DONE**
FIXME:**DONE**
    make maze use the practical version
    adapt Explore for practical version maze
FIXME:**DONE**
    fix the greedy search endless loop
    fix the deviation if possible
    fix the branch counting problem
"""

import queue
import math

class Node(object): #needed for new style class
    def __init__(self, coords, parent, dist):
        self.x = coords[0]
        self.y = coords[1]
        self.parent = parent
        self.pathDistance = dist #The cost
        self.children = [] #neighbours to expand into
        
    def addChild(self, child = []):
        child[0].parent = self
        self.children.append(child[0])
    def __lt__(self, other):
        return self.pathDistance < other.pathDistance
    
class AStarNode(Node):
    def __init__(self, coords, parent, pathDistance, euclidean):
        self.x = coords[0]
        self.y = coords[1]
        self.parent = parent
        self.pathDistance = pathDistance
        self.euclidean = euclidean #extra field to since A* combines h(n) and g(n)
        self.children = []
        
    def __lt__(self, other):
        return self.pathDistance + self.euclidean < other.pathDistance + other.euclidean
                  
class Tree(object): 
    """
    maze is a 2D array
    Will offer no checking for correct input
    """
    def __init__(self, maze):
        self.explored = []
        self.maze = maze #Shallow copy but fine for this practical
        #Potential porblem if the maze array passed in is edited outside
      
    """
    returns deep copy clone of self.maze
    """
    def mazeClone(self):
        clone = [[0 for i in range(len(self.maze))] for j in range(len(self.maze[0]))]
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (self.maze[i][j] == 1):
                    clone[i][j] = "|" #| = wall
        return clone
    
    """
    conveniently returns the boolean of whether given coords exist in self.explored which is the closet set
    """    
    def isExplored(self, coords):
        out  = False
        i = 0
        while (i < len(self.explored) and out == False):
            if (self.explored[i][0] == coords[0] and self.explored[i][1] == coords[1]):
                out = True
            i += 1
        return out
    """
    returns straight line distance from p1 to p2
    """
    def getSLD(self, p1, p2):
        return math.sqrt(math.pow(p2[0]-p1[0], 2) + math.pow(p2[1]-p1[1], 2))
 
    """
    returns number of nodes in the tree
    """
    def DFScount(self, node):
        rest = [i for i in node.children]
        count  = 1
        for i in range(len(rest)):
            count += self.DFScount(rest[i])
        return count       
    
    def UniformCostSearch(self, start, end):
        return self.search(1, start, end)
    
    def GreedyBestSearch(self, start, end):
        return self.search(2, start, end)
    
    def AStarSearch(self, start, end):
        return self.search(3, start, end)
    
    """
    conveniently creates the practical's result plot in a maze clone
    """
    def printPath(self, node, end, viewed, solution, found):
        
        solution[end[0]][end[1]] = "G" #G = goal
        if found ==  True and (node.x != end[0] or node.y != end[1]):
            solution[node.x][node.y] = "*"
        curr = node.parent
        
        while (curr != None):
            if (curr.parent == None):
                solution[curr.x][curr.y] = "S" #S = start
            elif found == True:
                solution[curr.x][curr.y] = "*" #* = path
            curr = curr.parent
        
        while (not viewed.empty()):
            vnode = viewed.get()
            if (solution[vnode.x][vnode.y] == 0):
                solution[vnode.x][vnode.y] = "V"#V = visited
                
        self.printMaze(solution)
        
        self.explored = []
    
    """
    prints a given maze(2D array) with contents intact
    """
    def printMaze(self, maze):
        out = "| "
        for i in range(len(maze[0])):
            out+= "- " 
        out += "|\n"
        for x in range(len(maze)):
            out += "| "
            for y in range(len(maze[x])):
                out += str(maze[x][y]) + " "
            out += "|\n"
        out += "| "
        for j in range(len(maze[0])):
            out+= "- " 
        out += "|\n"    
        print(out)
        
    """
    Implements all the searches in 1 function
    Method:
        case 1: Uniform cost
        case 2: Greedy Best search
        case 3: A* search
    
    """
    def search(self, method, start, end):
        if method < 1 or method > 3:
            print("Invalid Search method @ func search")
            return
        root = None
        title = ""
        if method == 1:
            root = Node(start, None, float(0))
            title = "Uniform Cost Search"
        elif method == 2:
            root = Node(start, None, float(self.getSLD(start, end)))
            title = "Greedy Best Search"
        elif method == 3:
            root = AStarNode(start, None, float(0), float(self.getSLD(start, end)))
            title = "A* Search"
        
        unvisited = queue.PriorityQueue() #open set or frontier
        self.explored = [] #closed set
        solution = self.mazeClone()
        unvisited.put(root)
        while (not unvisited.empty()):
            curr = unvisited.get()
            if (self.isExplored([curr.x, curr.y])):
                continue; # skip cycle if this block has already been expanded
            solution[curr.x][curr.y] = "X"
            self.explored.append([curr.x, curr.y])
            
            if (curr.x == end[0] and curr.y == end[1]):
                print(title+ ": " + str(self.DFScount(root)-1) + " nodes")
                print("Frontier = " + str(unvisited.qsize()) + " nodes")
                return self.printPath(curr, end, unvisited, solution, True)
            children = self.explore(curr) # all neighbour coordinates that can be expanded into
            for i in range(len(children)):
                if method == 1:
                    curr.addChild([Node(children[i], None, curr.pathDistance + float(self.getSLD([curr.x, curr.y], children[i])))])
                elif method == 2:
                    curr.addChild([Node(children[i], None, float(self.getSLD(children[i], end)))])
                elif method == 3:
                    curr.addChild([AStarNode(children[i], None, float(curr.pathDistance + self.getSLD([curr.x, curr.y], children[i])), float(self.getSLD(children[i], end)))])
            for j in range(len(children)):    
                unvisited.put(curr.children[j])
        print(title+ ": " + str(self.DFScount(root)-1) + " nodes")
        print("Frontier = " + str(unvisited.qsize()) + " nodes")        
        print("No " + title + " solution found")
        return self.printPath(curr, end, unvisited, solution, False)
    
    """
    returns coords of all expandable nodes
    add in clockwise fashion from up
    """
    def explore(self, node):
        x = node.x
        y = node.y
        out = []
        
        if (y < len(self.maze[0])-1):
            if (not self.isExplored([x, y+1])) and self.maze[x][y+1] == 0:#check up
                out.append([x, y+1])
            if x < len(self.maze)-1 and (not self.isExplored([x+1, y+1])) and self.maze[x+1][y+1] == 0:#check diag up, right
                out.append([x+1, y+1])
                
        if (x < len(self.maze)-1 and self.maze[x+1][y] == 0 and not self.isExplored([x+1, y])):#check right
            out.append([x+1, y])
        
        if (y > 0):
            if x < len(self.maze)-1 and (not self.isExplored([x+1, y-1])) and self.maze[x+1][y-1] == 0:#check diag down, right
                out.append([x+1, y-1])
            if (not self.isExplored([x, y-1])) and self.maze[x][y-1] == 0:#check down
                out.append([x, y-1])            
            if x > 0 and (not self.isExplored([x-1, y-1])) and self.maze[x-1][y-1] == 0:#check diag down, left
                out.append([x-1, y-1])
        
        if (x > 0 and self.maze[x-1][y] == 0 and not self.isExplored([x-1, y])):#check left
            out.append([x-1, y])
        
        if (y < len(self.maze[0])-1):        
            if x > 0 and (not self.isExplored([x-1, y+1])) and self.maze[x-1][y+1] == 0:#check diag up, left
                out.append([x-1, y+1])
        return out
        

maze = [[0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,1,1,1,0,1,1,0],
        [0,1,0,0,0,0,1,1,0,1,1,0],
        [0,1,1,0,0,0,0,0,0,1,1,0],
        [0,1,1,1,0,0,0,0,0,1,1,0],
        [0,1,1,1,1,0,0,0,0,1,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0]]

tree = Tree(maze)
tree.UniformCostSearch([0, 0], [9, 9])
tree.GreedyBestSearch([0, 0], [9, 9])
tree.AStarSearch([0, 0], [9, 9])
