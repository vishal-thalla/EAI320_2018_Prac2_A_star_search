# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:12:59 2018

@author: Sirshen Munsamy
"""
from queue import PriorityQueue

class Block(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev = None       
        self.surrounds = []
        
    def surround(self, found):
        self.surrounds.append(found[0])
        found[0].prev = self
        
    def setcost(self, cost):
        self.cost = cost
    
    def setgreedy(self, greedy):
        self.greedy = greedy
    
    
    def __lt__(self, compare):
        compare

class Search(object):
    def __init__(self, array):
        self.array = array
        self.openset = PriorityQueue()
        self.closedset = []
        
    def duplicate(self, block):
        for i in self.closedset:
            if (i.x == block.x and i.y == block.y):
                return True
        return False

    def getblock(self, x, y, cost, greedy):
        temp = Block(x, y)
        temp.setgreedy(greedy)
        temp.setcost(cost)
        return temp
    
    
    def UniformCostSearch(self, sx, sy, gx, gy): 
        #https://algorithmicthoughts.wordpress.com/2012/12/15/artificial-intelligence-uniform-cost-searchucs/ for pseudocode
        start = self.getblock(sx, sy, 0, 0)
        self.openset.put(start)
        while (not self.openset.empty()):
            block = self.openset.get()
            self.closedset.append(block)
            self.array[block.x][block.y] = "1"
            if (block.x == gx and block.y == gy):
                print("Uniform Cost search")
                return self.show(block.x, block.y, gx, gy)
            surrounds = self.uniformsurrounds(block)            
            children = [i for i in surrounds if not self.duplicate(i)]
            for i in range(len(children)):
                block.surround([children[i]])
                self.openset.put(block.surrounds[i])
                
    def uniformsurrounds(self, block):

        surrounds = []
        
        if block.y < len(self.array[0])-1 and self.array[block.x][block.y+1] == 0:
            surrounds.append(self.getblock(block.x,block.y+1, block.cost + 1, 0))
        if block.y < len(self.array[0])-1 and block.x < len(self.array)-1 and self.array[block.x+1][block.y+1] == 0:
            surrounds.append(self.getblock(block.x+1,block.y+1, block.cost + float(pow(2, float(1/2))), 0))
        if block.x < len(self.array)-1 and self.array[block.x+1][block.y] == 0:
            surrounds.append(self.getblock(block.x+1,block.y, block.cost + 1, 0))
        if block.y > 0 and self.array[block.x][block.y-1] == 0:
            surrounds.append(self.getblock(block.x,block.y-1,block.cost + 1, 0))
        if block.y > 0 and block.x < len(self.array)-1 and self.array[block.x+1][block.y-1] == 0:
            surrounds.append(self.getblock(block.x+1,block.y-1, block.cost + float(pow(2, float(1/2))), 0))
        if block.y > 0 and block.x > 0 and self.array[block.x-1][block.y-1] == 0:
            surrounds.append(self.getblock(block.x-1,block.y-1, block.cost + float(pow(2, float(1/2))), 0))
        if block.x > 0 and self.array[block.x-1][block.y] == 0:
            surrounds.append(self.getblock(block.x-1,block.y, block.cost + 1, 0))
        if block.y < len(self.array[0])-1 and block.x > 0 and self.array[block.x-1][block.y+1] == 0:
            surrounds.append(self.getblock(block.x-1,block.y+1, block.cost + float(pow(2, float(1/2))),0))
        return surrounds   
                
    def GreedySearch(self, sx, sy, gx, gy): 
        start = self.getblock(sx, sy, 0, 0)
        self.openset.put(start)
        while (not self.openset.empty()):
            block = self.openset.get()
            self.closedset.append(block)
            if (block.x == gx and block.y == gy):
                print("Greedy/Best search")
                return self.show(block.x, block.y, gx, gy)
            surrounds = self.greedysurrounds(block)            
            children = [i for i in surrounds if not self.duplicate(i)]
            for i in children:
                block.surround([i])
                self.openset.put(i)      
                
    def AstarSearch(self, sx, sy, gx, gy): 
        start = self.getblock(sx, sy, 0, 0)
        self.openset.put(start)
        while (not self.openset.empty()):
            block = self.openset.get()
            self.closedset.append(block)
            if (block.x == gx and block.y == gy):
                print("A Star search")
                return self.show(block.x, block.y, gx, gy)
            surrounds = self.astarsurrounds(block)            
            children = [i for i in surrounds if not self.duplicate(i)]
            for i in children:
                block.surround([i])
                self.openset.put(i)  
                
    def astarsurrounds(self, block):
        surrounds = []
        
        if block.y < len(self.array[0])-1 and self.array[block.x][block.y+1] == 0:
            surrounds.append(self.getblock(block.x,block.y+1, block.cost +1, self.pythagoras(block.x, block.y+1)))
        if block.y < len(self.array[0])-1 and block.x < len(self.array)-1 and self.array[block.x+1][block.y+1] == 0:
            surrounds.append(self.getblock(block.x+1,block.y+1, block.cost + float(pow(2, float(1/2)), self.pythagoras(block.x+1, block.y+1))))
        if block.x < len(self.array)-1 and self.array[block.x+1][block.y] == 0:
            surrounds.append(self.getblock(block.x+1,block.y, block.cost +1, self.pythagoras(block.x+1, block.y)))
        if block.y > 0 and self.array[block.x][block.y-1] == 0:
            surrounds.append(self.getblock(block.x,block.y-1, block.cost + float(pow(2, float(1/2)), self.pythagoras(block.x, block.y-1))))
        if block.y > 0 and block.x < len(self.array)-1 and self.array[block.x+1][block.y-1] == 0:
            surrounds.append(self.getblock(block.x+1,block.y-1, block.cost +1, self.pythagoras(block.x+1, block.y-1)))
        if block.y > 0 and block.x > 0 and self.array[block.x-1][block.y-1] == 0:
        		surrounds.append(self.getblock(block.x-1,block.y-1, block.cost + float(pow(2, float(1/2)), self.pythagoras(block.x-1, block.y-1))))
        if block.x > 0 and self.array[block.x-1][block.y] == 0:
            surrounds.append(self.getblock(block.x-1,block.y, block.cost +1, self.pythagoras(block.x-1, block.y)))
        if block.y < len(self.array[0])-1 and block.x > 0 and self.array[block.x-1][block.y+1] == 0:
            surrounds.append(self.getblock(block.x-1,block.y+1, block.cost + float(pow(2, float(1/2)), self.pythagoras(block.x-1, block.y+1))))
        return surrounds  
    
    def greedysurrounds(self, block):

        surrounds = []
        
        if block.y < len(self.array[0])-1 and self.array[block.x][block.y+1] == 0:
            surrounds.append(self.getblock(block.x,block.y+1, 0, self.pythagoras(block.x, block.y+1)))
        if block.y < len(self.array[0])-1 and block.x < len(self.array)-1 and self.array[block.x+1][block.y+1] == 0:
            surrounds.append(self.getblock(block.x+1,block.y+1, 0, self.pythagoras(block.x+1, block.y+1), 0))
        if block.x < len(self.array)-1 and self.array[block.x+1][block.y] == 0:
            surrounds.append(self.getblock(block.x+1,block.y, 0, self.pythagoras(block.x+1, block.y)))
        if block.y > 0 and self.array[block.x][block.y-1] == 0:
            surrounds.append(self.getblock(block.x,block.y-1, 0, self.pythagoras(block.x, block.y-1)))
        if block.y > 0 and block.x < len(self.array)-1 and self.array[block.x+1][block.y-1] == 0:
            surrounds.append(self.getblock(block.x+1,block.y-1, 0, self.pythagoras(block.x+1, block.y-1)))
        if block.y > 0 and block.x > 0 and self.array[block.x-1][block.y-1] == 0:
            surrounds.append(self.getblock(block.x-1,block.y-1, 0, self.pythagoras(block.x-1, block.y-1)))
        if block.x > 0 and self.array[block.x-1][block.y] == 0:
            surrounds.append(self.getblock(block.x-1,block.y, 0, self.pythagoras(block.x-1, block.y)))
        if block.y < len(self.array[0])-1 and block.x > 0 and self.array[block.x-1][block.y+1] == 0:
            surrounds.append(self.getblock(block.x-1,block.y+1, 0, self.pythagoras(block.x-1, block.y+1)))
        return surrounds  
		
    
    def show(self, sx, sy, gx, gy):        
        temp = self.closedset[len(self.closedset)-2]       
        while (self.openset.qsize() > 0):
            temp =  self.openset.get()
            if (self.array[temp.x][temp.y] == 0):
                self.array[temp.x][temp.y] = "2"                
        while (temp.prev != None):
            self.array[temp.x][temp.y] = "*"
            temp = temp.prev   
        self.array[sx][sy] = "S"
        self.array[gx][gy] = "G"
        for x in range(len(self.array)):
            out = ""
            y = 0
            for y in range(len(self.array[0])-1):
                out += str(self.array[x][y]) + ","
            out += str(self.array[x][y])
            print(out)
        
        self.openset = PriorityQueue()
        self.closedset = []
    
    def pythagoras(self, sx, sy, gx, gy):
        result = float(pow(pow(gx - sx, 2) + pow(gy - sy, 2), float(1/2)))
        return result
    

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

tree = Search(maze)
tree.UniformCostSearch(0, 0, 9, 9)
#tree2 = Search(maze)
#tree2.GreedySearch(0, 0, 9, 9)
#tree.AstarSearch(0, 0, 9, 9)