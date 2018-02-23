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
FIXME:
    fix the greedy search endless loop
    fix the deviation if possible
    fix the branch counting problem // NOTE: issue might be due to the Explore function returning nodes directly
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
            self.addChild([children[i]])
      
    #don't clutter the tree unnecessarily since there is no delete method    
    def addChild(self, child = []):
        if (self.find(child[0].x, child[0].y) == len(self.children)): # not found
            child[0].parent = self
            self.children.append(child[0])
    def __lt__(self, other):
        return self.pathDistance < other.pathDistance
    
class AStarNode(Node):
    def __init__(self, x, y, parent, pathDistance, euclidean):
        self.x = x
        self.y = y
        self.parent = parent
        self.pathDistance = pathDistance
        self.euclidean = euclidean
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
        #Potential problem if the maze array passed in is edited outside
        
    def mazeClone(self):
        clone = [[0 for i in range(len(self.maze))] for j in range(len(self.maze[0]))]
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (self.maze[i][j] == 1):
                    clone[i][j] = "|"
        return clone
    
    def printPath(self, node, end, viewed, solution):
        
        solution[end[0]][end[1]] = "G"
        if (node.x != end[0] or node.y != end[1]):
            solution[node.x][node.y] = "*"
        curr = node.parent
        
        while (curr != None):
           if (curr.parent == None):
               solution[curr.x][curr.y] = "S"
           else:
               solution[curr.x][curr.y] = "*"
           curr = curr.parent
#        print("Before adding Viewed")
#        self.printMaze(solution)
        
        while (not viewed.empty()):
            vnode = viewed.get()
            if (solution[vnode.x][vnode.y] == 0):
                solution[vnode.x][vnode.y] = "V"
        
#        print("After adding Viewed")
        self.printMaze(solution)
        
        self.explored = []
        
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
    
    def isExplored(self, coords):
        out  = False
        i = 0
        while (i < len(self.explored) and out == False):
            if (self.explored[i].x == coords[0] and self.explored[i].y == coords[1]):
                out = True
            i += 1
        return out
    """
    returns straight line distance from p1 to p2
    """
    def getSLD(self, p1, p2):
        return math.sqrt(math.pow(p2[0]-p1[0], 2) + math.pow(p2[1]-p1[1], 2))
    
    def BFScount(self, start):
        unvisited = queue.Queue()
        unvisited.put(start)
        count = 0
        
        while(not unvisited.empty()):
            curr = unvisited.get()
            count += 1
            rest = [i for i in curr.children]
            for i in rest:
                unvisited.put(i)
        return count
    
    def DFScount(self, node):
        rest = [i for i in node.children]
        count  = 1
        for i in range(len(rest)):
            count += self.DFScount(rest[i])
        return count
        
    def AStarSearch(self, start, end):
        root = AStarNode(start[0], start[1], None, 0, self.getSLD(start, end))
        unvisited = queue.PriorityQueue()
        self.explored = []
        solution = self.mazeClone()
        unvisited.put(root)
        count = 0
        while (not unvisited.empty()):
            curr = unvisited.get()
            solution[curr.x][curr.y] = "X"
            self.explored.append(curr)
            if (curr.x == end[0] and curr.y == end[1]):
                print("A*: " + " count "+ str(count) + " nodes")
                return self.printPath(curr, end, unvisited, solution)
            children = self.astarExplore(curr, end)
            if (len(children) == 0 and unvisited.empty()):
                print("No A* Solution found")
                return self.printPath(curr, end, unvisited, solution)
            curr.addChildren(children)
            for i in children:
                count += 1
                unvisited.put(i)
        
                
    def astarExplore(self, node, end):
        x = node.x
        y = node.y
        out = []
        
        if (y < len(maze[x])-1):
            if (not self.isExplored([x, y+1])) and self.maze[x][y+1] == 0:#check up
                out.append(AStarNode(x, y+1, node, node.pathDistance + 1, self.getSLD([x, y+1], end)))
            if x < len(maze)-1 and (not self.isExplored([x+1, y+1])) and self.maze[x+1][y+1] == 0:#check diag up, right
                out.append(AStarNode(x+1, y+1, node, node.pathDistance + math.sqrt(2), self.getSLD([x+1, y+1], end)))
            if x > 0 and (not self.isExplored([x-1, y+1])) and self.maze[x-1][y+1] == 0:#check diag up, left
                out.append(AStarNode(x-1, y+1, node, node.pathDistance + math.sqrt(2), self.getSLD([x-1, y+1], end)))
        if (y > 0):
            if (not self.isExplored([x, y-1])) and self.maze[x][y-1] == 0:#check down
                out.append(AStarNode(x, y-1, node, node.pathDistance + 1, self.getSLD([x, y-1], end)))
            if x < len(maze)-1 and (not self.isExplored([x+1, y-1])) and self.maze[x+1][y-1] == 0:#check diag down, right
                out.append(AStarNode(x+1, y-1, node, node.pathDistance + math.sqrt(2),self.getSLD([x+1, y-1], end)))
            if x > 0 and (not self.isExplored([x-1, y-1])) and self.maze[x-1][y-1] == 0:#check diag down, left
                out.append(AStarNode(x-1, y-1, node, node.pathDistance + math.sqrt(2), self.getSLD([x-1, y-1], end)))
        
        if (x < len(self.maze)-1 and self.maze[x+1][y] == 0 and not self.isExplored([x+1, y])):#check right
            out.append(AStarNode(x+1, y, node, node.pathDistance + 1, self.getSLD([x+1, y], end)))
        if (x > 0 and self.maze[x-1][y] == 0 and not self.isExplored([x-1, y])):#check left
            out.append(AStarNode(x-1, y, node, node.pathDistance + 1, self.getSLD([x-1, y], end)))
        return out  
        
    def UniformCostSearch(self, start, end): # start and end are 2 element arrays for respective coords
        root = Node(start[0], start[1], None, 0)
        unvisited = queue.PriorityQueue()
        self.explored = []
        solution = self.mazeClone()
        unvisited.put(root)
        count = 0
        while (not unvisited.empty()):
            curr = unvisited.get()
            solution[curr.x][curr.y] = "X"
            self.explored.append(curr)
            if (curr.x == end[0] and curr.y == end[1]):
                print("Uniform cost: "+ " count " + str(count) + " nodes")
                return self.printPath(curr, end, unvisited, solution)
            children = self.uniformExplore(curr)
            if (len(children) == 0 and unvisited.empty()):
                print("No Uniform cost Solution found")
                return self.printPath(curr, end, unvisited, solution)
            curr.addChildren(children)
            for i in children:
                count += 1
                unvisited.put(i)
                
    def uniformExplore(self, node):
        """
        Boundary conditions:
            top and bottom corners and edges
            side edges
        """
        x = node.x
        y = node.y
        out = []
        
        if (y < len(maze[x])-1):
            if (not self.isExplored([x, y+1])) and self.maze[x][y+1] == 0:#check up
                out.append(Node(x, y+1, node, node.pathDistance + 1))
            if x < len(maze)-1 and (not self.isExplored([x+1, y+1])) and self.maze[x+1][y+1] == 0:#check diag up, right
                out.append(Node(x+1, y+1, node, node.pathDistance + math.sqrt(2)))
            if x > 0 and (not self.isExplored([x-1, y+1])) and self.maze[x-1][y+1] == 0:#check diag up, left
                out.append(Node(x-1, y+1, node, node.pathDistance + math.sqrt(2)))
        if (y > 0):
            if (not self.isExplored([x, y-1])) and self.maze[x][y-1] == 0:#check down
                out.append(Node(x, y-1, node, node.pathDistance + 1))
            if x < len(maze)-1 and (not self.isExplored([x+1, y-1])) and self.maze[x+1][y-1] == 0:#check diag down, right
                out.append(Node(x+1, y-1, node, node.pathDistance + math.sqrt(2)))
            if x > 0 and (not self.isExplored([x-1, y-1])) and self.maze[x-1][y-1] == 0:#check diag down, left
                out.append(Node(x-1, y-1, node, node.pathDistance + math.sqrt(2)))
        
        if (x < len(self.maze)-1 and self.maze[x+1][y] == 0 and not self.isExplored([x+1, y])):#check right
            out.append(Node(x+1, y, node, node.pathDistance + 1))
        if (x > 0 and self.maze[x-1][y] == 0 and not self.isExplored([x-1, y])):#check left
            out.append(Node(x-1, y, node, node.pathDistance + 1))
        return out   
                
    def GreedyBestSearch(self, start, end):
        root = Node(start[0], start[1], None, self.getSLD(start, end))
        unvisited = queue.PriorityQueue()
        self.explored = []
        solution = self.mazeClone()
        unvisited.put(root)
        count = 0
        while (not unvisited.empty()):
            curr = unvisited.get()
            solution[curr.x][curr.y] = "X"
            self.explored.append(curr)
            if (curr.x == end[0] and curr.y == end[1]):
                print("Greedy Best: " + " count " + str(count) + " nodes")
                return self.printPath(curr, end, unvisited, solution)
            children = self.greedyExplore(curr, end)
            if (len(children) == 0 and unvisited.empty()):
                print("No Greedy Best Solution found: empty")
                return self.printPath(curr, end, unvisited, solution)
            curr.addChildren(children)
            for i in children:
                count += 1
                unvisited.put(i)
#            prev = curr            
    
    def greedyExplore(self, node, end):
        """
        Boundary conditions:
            top and bottom corners and edges
            side edges
        """
        x = node.x
        y = node.y
        out = []
        
        if (y < len(maze[x])-1):
            if (not self.isExplored([x, y+1])) and self.maze[x][y+1] == 0:#check up
                out.append(Node(x, y+1, node, self.getSLD([x, y+1], end)))
            if x < len(maze)-1 and (not self.isExplored([x+1, y+1])) and self.maze[x+1][y+1] == 0:#check diag up, right
                out.append(Node(x+1, y+1, node, self.getSLD([x+1, y+1], end)))
            if x > 0 and (not self.isExplored([x-1, y+1])) and self.maze[x-1][y+1] == 0:#check diag up, left
                out.append(Node(x-1, y+1, node, self.getSLD([x-1, y+1], end)))
        if (y > 0):
            if (not self.isExplored([x, y-1])) and self.maze[x][y-1] == 0:#check down
                out.append(Node(x, y-1, node, self.getSLD([x, y-1], end)))
            if x < len(maze)-1 and (not self.isExplored([x+1, y-1])) and self.maze[x+1][y-1] == 0:#check diag down, right
                out.append(Node(x+1, y-1, node, self.getSLD([x+1, y-1], end)))
            if x > 0 and (not self.isExplored([x-1, y-1])) and self.maze[x-1][y-1] == 0:#check diag down, left
                out.append(Node(x-1, y-1, node, self.getSLD([x-1, y-1], end)))
        
        if (x < len(self.maze)-1 and self.maze[x+1][y] == 0 and not self.isExplored([x+1, y])):#check right
            out.append(Node(x+1, y, node, self.getSLD([x+1, y], end)))
        if (x > 0 and self.maze[x-1][y] == 0 and not self.isExplored([x-1, y])):#check left
            out.append(Node(x-1, y, node, self.getSLD([x-1, y], end)))
        
        return out   

maze = [[0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,1,1,0,1,1,0],
        [0,1,0,0,0,0,1,1,0,1,1,0],
        [0,1,1,0,0,0,0,0,0,1,1,0],
        [0,1,1,1,0,0,0,0,0,1,1,0],
        [0,1,1,1,1,0,0,0,0,1,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0]]

tree = Tree(maze)
tree.UniformCostSearch([0, 0], [9, 9])
tree.GreedyBestSearch([0, 0], [9, 9])
tree.AStarSearch([0, 0], [9, 9])
