# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 17:41:43 2018

@author: Vishal Thalla(16053525)
"""
import math
class Node(object): #needed for new style class
    def __init__(self, coords, parent, dist):
        self.x = coords[0]
        self.y = coords[1]
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
        child[0].parent = self
        self.children.append(child[0])
    def __lt__(self, other):
        return self.pathDistance < other.pathDistance
    
class Tree(object):
    def __init__(self, maze):
        self.explored = []
        self.maze = maze #Shallow copy but fine for this practical
        #Potential porblem if the maze array passed in is edited outside
    def mazeClone(self):
        clone = [[0 for i in range(len(self.maze))] for j in range(len(self.maze[0]))]
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (self.maze[i][j] == 1):
                    clone[i][j] = "|" #| = wall
        return clone
    
    def printPath(self, node, end, viewed, solution):
        
        solution[end[0]][end[1]] = "G" #G = goal
        curr = node.parent
        
        while (curr != None):
            if (curr.parent == None):
                solution[curr.x][curr.y] = "S" #S = start
            else:
                solution[curr.x][curr.y] = "*" #* = path
            curr = curr.parent
        
        while (len(viewed) > 0):
            vnode = viewed.pop(len(viewed)-1)
            if (solution[vnode.x][vnode.y] == 0):
                solution[vnode.x][vnode.y] = "V"#V = visited
                
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

        if coords in self.explored:
            print('T')
            return True
        print('F')
        return False
    def getSLD(self, p1, p2):
        return float(math.sqrt(math.pow(p2[0]-p1[0], 2) + math.pow(p2[1]-p1[1], 2)))
    
    def DFScount(self, node):
        rest = [i for i in node.children]
        count  = 1
        for i in range(len(rest)):
            count += self.DFScount(rest[i])
        return count
    
    def UniformCostSearch(self, start, end):
        root = Node(start, None, float(0))
        unvisited = []
        self.explored = []
        solution = self.mazeClone()
        unvisited.extend([root])
        while (len(unvisited) > 0):
            curr = unvisited.pop(0)
            if (self.isExplored([curr.x, curr.y])):
                continue;
            solution[curr.x][curr.y] = 'X'
            self.explored.append([curr.x, curr.y])
            if (curr.x == end[0] and curr.y == end[1]):
                print(str(len(self.explored)))
                print(str(self.DFScount(root)-1))
                print(self.explored)
                return self.printPath(curr, end, unvisited, solution)
            children = self.explore(curr)
            for i in range(len(children)):
                if (self.isExplored(children[i]) == False):
                    curr.addChild([Node(children[i], None, curr.pathDistance + float(self.getSLD([curr.x, curr.y], children[i])))])
                    unvisited.extend([curr.children[i]])
            unvisited =  sorted(unvisited)
    
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