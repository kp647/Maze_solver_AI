import random
import numpy as np
import sys
sys.setrecursionlimit(10000)


def dirx (data):

    if data == 'north':
        return 0
    elif data =='south':
        return 0
    elif data == 'east':
        return 1
    elif data == "west":
        return -1
    else:
        return -1
def diry (data):
    if data == "east":
        return 0
    if data == "west":
        return 0
    if data == "north":
        return 1
    if data == "south":
        return -1
def oppo(data):
    if data == "west":
        return "east"
    if data == "east":
        return "west"
    if data == "north":
        return "south"
    if data == "south":
        return "north"
def getnum(data):
    if data == "west":
        return 4
    if data == "east":
        return 3
    if data == "north":
        return 1
    if data == "south":
        return 2
north=1
south=2
east=3
west=4
def ispath(grid,x,y,dirAllowed):
    if dirAllowed!= 'north' and y<100:
        if grid[x][y+1]!=0:
            return False
    if dirAllowed!= 'south':
        if grid[x][y-1]!=0 and y>0:
            return False
    if dirAllowed!= 'east' and x<100:
        if grid[x+1][y]!=0:
            return False
    if dirAllowed!= 'west' and x>0:
        if grid[x-1][y]!=0:
            return False
    return True

grid1=np.zeros([101,101],dtype=int)
def make_passages(x,y,grid):
    directions=["north","south","east","west"]
    random.shuffle(directions)
   # print directions
    for number in directions:
        newx= x+dirx(number)
        newy=y+diry(number)
        #print (newx >= 0 and newx < 101) and (newy >= 0 and newy < 101) and grid[newy][newx]==0
        if newx >= 0 and newx < 101 and newy >= 0 and newy < 101 and grid[newx][newy]==0 and ispath(grid,newx,newy,oppo(number)):
            grid[x][y]=1 #getnum(number)
           # print getnum(number)
            #print number + "came in here"
            grid[newx][newy]=1#getnum(oppo(number))
           # print "hiiiiiii"
           # print getnum(oppo(number))

            make_passages(newx, newy,grid)
make_passages(0,0,grid1)
print grid1


#directions=[north,south,east,west]
#random.shuffle(directions)
#print directions