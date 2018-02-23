# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 18:04:05 2018

@author: Vishal Thalla(16053525)
"""
"""
TODO:
    adapt Node class for this practical
    create Uniform cost function:**DONE**
    create Greedy Best search
    create A* search by figuring how to combine Uniform cost and Greedy Best
FIXME:
    make maze use the practical version
    adapt Explore for practical version maze
"""

import queue
import math

class Node(object): #needed for new style class
    #class will only hold a value which will be title and children nodes
    def __init__(self, x, y, parent, dist):
        self.x = x
        self.y = y
        self.parent = parent
        self.pathDistance = dist
        self.children = []
        
    """
    returns index of node(value) in self.children
    """
    def find(self, x, y):
        i = 0
        while (i != len(self.children) and self.children[i].x != x and self.children[i].y != y):
            i += 1
        return i
    
    def hasChild(self, value):
        if (self.find(value) == len(self.children)):
            return False
        return True
    
    def addChildren(self, children = []):
        for i in range(len(children)):
            self.addChild(children[i])
      
    #don't clutter the tree unnecessarily since there is no delete method    
    def addChild(self, child):
        if (self.find(child.x, child.y) == len(self.children)): # not found
            child.parent = self
            self.children.append(child)
    def __lt__(self, other):
        return self.pathDistance < other.pathDistance
            
#    def __cmp__(self, other):
#        if (self.pathDistance < other.pathDistance):
#            return -1
#        if (self.pathDistance == other.pathDistance):
#            return 0
#        if (self.pathDistance > other.pathDistance):
#            return 1
            
class Tree(object): 
    """
    maze is a 2D array from // needs to be ordered as top-left = 0, 0 and top right = 0, width-1
    Will offer no checking for correct input
    """
    def __init__(self, maze):
        self.explored = []
        self.maze = maze #Shallow copy but fine for this practical
        #Potential porblem if the maze array passed in is edited outside
        
    
    
    def UniformCostSearch(self, start, end): # start and end are 2 element arrays for respective coords
#        Sx = start[0], Sy = start[1]
#        Gx = end[0], Gy = end[1]
        root = Node(start[0], start[1], None, 0)
        unvisited = queue.PriorityQueue()
        self.explored = []
        
        unvisited.put(root)
        while (not unvisited.empty()):
            curr = unvisited.get()
            self.explored.append(curr)
            if (curr.x == end[0] and curr.y == end[1]):
                return self.printPath(curr)
            children = self.Explore(curr)
            curr.addChildren(children)
            for i in range(len(children)):
                unvisited.put(children[i])
    
    def printPath(self, node):
        out = "[" + str(node.x) + "," + str(node.y) + "]"
        curr = node.parent
        while (curr != None):
            out = "[" + str(curr.x) + "," + str(curr.y) + "]\n" + out
            curr = curr.parent
        print(out)
    
    def isExplored(self, coords):
        out  = False
        i = 0
        while (i < len(self.explored) and out == False):
            if (self.explored[i].x == coords[0] and self.explored[i].y == coords[1]):
                out = True
            i += 1
        return out
            
    """
    NOTE: swaps x and y
    """
    def Explore(self, node):
        """
        Boundary conditions:
            top and bottom corners and edges
            side edges
        """
        x = node.x
        y = node.y
        #out = [0 for i in range(8)] # 8 0s
        out = []
        
        if (y != 0):
            if (self.maze[y-1][x] == 0 and not self.isExplored([x, y-1])): #check up
                out.append(Node(x, y-1, node, node.pathDistance + 1))
            if (x != len(self.maze[y])-1 and self.maze[y-1][x+1] == 0 and not self.isExplored([x+1, y-1])): #check diagonal up, right
                out.append(Node(x+1,y-1, node, node.pathDistance + math.sqrt(2)))
            if (x != 0 and self.maze[y-1][x-1] == 0 and not self.isExplored([x-1, y-1])): #check diagonal up, left
                out.append(Node(x-1, y-1, node, node.pathDistance + math.sqrt(2)))
            
        if (y != len(self.maze)-1):
            if (self.maze[y+1][x] == 0 and not self.isExplored([x, y+1])):#check down
                out.append(Node(x, y+1, node, node.pathDistance + 1))
            if (x != len(self.maze[y])-1 and self.maze[y+1][x+1] == 0 and not self.isExplored([x+1,y+1])):#check diagonal down, right
                out.append(Node(x+1, y+1,  node, node.pathDistance + math.sqrt(2)))
            if (x != 0 and self.maze[y+1][x-1] == 0 and not self.isExplored([x-1, y+1])):#check diagonal down, left
                out.append(Node(x-1, y+1, node, node.pathDistance + math.sqrt(2)))
                
        if (x != len(self.maze)-1 and self.maze[y][x+1] == 0 and not self.isExplored([x+1, y])):#check right
            out.append(Node(x+1, y, node, node.pathDistance + 1))
        
        if (x != 0 and self.maze[y][x-1] == 0 and not self.isExplored([x-1, y])):#check left
            out.append(Node(x-1, y, node, node.pathDistance + 1))
            
        return out    

maze = [[0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1,0,0,1,0],
        [0,0,0,0,0,0,1,1,0,0,1,0],
        [0,1,1,0,0,0,1,1,0,0,1,0],
        [0,1,1,0,0,0,1,1,0,0,1,0],
        [0,1,0,0,0,0,1,1,0,0,1,0],
        [0,0,0,0,0,1,1,1,0,0,1,0],
        [0,0,0,0,1,1,1,1,0,0,1,0],
        [0,0,0,1,1,1,1,1,0,0,1,0],
        [0,0,1,1,1,1,1,1,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0]]

tree = Tree(maze)
tree.UniformCostSearch([0, 11], [9, 2])
