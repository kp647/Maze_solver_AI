import numpy as np
from heapq import *
import pygame
import os
from datetime import datetime
#Node class
class Node:
    def __init__(self,data,num,x,y,path):
        # type: (object) -> object
        self.cellnum = num
        self.unblocked=data
        self.x=x
        self.y=y
        self.path=path
        self.agentp=0
        self.projected_path=0
        self.start=0
        self.target=0
    def getobs(self):
        return self.obs
    def getcellnum(self):
        return self.cellnum
    def getblockstatus(self):
        return self.unblocked
    def getx(self):
        return self.x
    def gety(self):
        return  self.y
    def ispath(self):
        return self.path
    def setpath(self,number):
        self.path=number
    def setblockstatus(self,data):
        self.unblocked=data
    def getagentpath(self):
        return self.agentp
    def setagentpath(self,p):
        self.agentp=p
    def getprojectedpath(self):
        return self.projected_path
    def setprojectedpath(self,p):
        self.projected_path=p
    def gettarget(self):
        return self.target
    def settarget(self,p):
        self.target=p
    def getstart(self):
        return self.start
    def setstart(self,p):
        self.start=p

#returns hvalue
def gethuristic(cellA,cellB):
    distance= abs(cellB.getx()-cellA.getx())+abs(cellB.gety()-cellA.gety())
    return distance

##prints final path
def printfinalpath(path):
    for i in path:
        print (str(i.getx()) + "   " + str(i.gety()))

#prints final path and sets node atribute path to =1
def printfinalactualpath(path):
    for i in path:
        print (str(i.getx()) + "   " + str(i.gety()))
        i.setpath(1)
#takes list and returns final path
def create_final_path(path):
    fin_path=[]


    i=0
    while i < len(path):
        j=i+1
       # print i
        fin_path.append(path[i])
        while j < len(path):
            if (path[i].getx() == path[j].getx() and path[i].gety() == path[j].gety()) or path[j] in fin_path:
                #print"found duplicate"
                i=j
                break
            j+=1
        i+=1
    return fin_path

#resets projected path
def reset_projected_path(path):
    for i in path:
        i.setprojectedpath(0)

#returns new hscore
def get_new_hscore(start,target,hscore):
    if hscore[start.getcellnum()] == float("inf"):
        return gethuristic(start,target)
    else:
        return hscore[start.getcellnum()]
#updates surroundings when agent moves
def update_surrounding(travelingGrid,grid,cell):
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for x, y in neighbors:
        if (cell.getx() + x) <= -1 or (cell.getx() + x) >= 101 or (
                cell.gety() + y) <= -1 or (
                cell.gety() + y) >= 101:
            continue
        if grid[cell.getx()+x][cell.gety()+y]==0:
            travelingGrid[cell.getx()+x][cell.gety()+y].setblockstatus(0)

#creates node grid of 101x101
def creategrid(grid):
    counter = 0
    for row in range(101):
        grid.append([])


        for column in range(101):
            grid[row].append(Node(1,counter,row,column,0))


            counter+=1

#reverses a list
def reverse_list(lis):
    templist=[]
    for i in list:
        templist.append(lis.pop())
    return templist
#shows maze while agent moves and the final path of which the robot travels/will travel
def show_new_maze(grid,travelingGrid,screen,start,target):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            showdisplay = False
            pygame.quit()
    screen.fill(BLACK)
    for row in range(101):
        for column in range(101):
            color = BLACK
            if grid[row][column] == 1:
                color = WHITE
            if grid[row][column] == 0:
                color = BLACK
                # grid2[row][column].setpath(1)
            if travelingGrid[row][column].getprojectedpath() == 1:
                color = BLUE
            if travelingGrid[row][column].getagentpath() == 1:
                color = BROWN
            if travelingGrid[row][column].ispath() == 1:
                color = GREEN
            if travelingGrid[row][column]== start:
                color= YELLOW
            if travelingGrid[row][column]== target:
                color= ORANGE
            # if row==0 or column ==0 or row==100 or column==100:
            # color=
            # print grid2[row][column]
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    pygame.display.flip()


#Main ()
def adaptive_a_astar(start, target, grid,newgrid):
    #show display toggle on/off visual of search
    showdisplay = True
    if showdisplay ==True:
        pygame.init()
        WINDOW_SIZE = [2048, 2048]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        for row in range(101):
            for column in range(101):
                color = BLACK
                if grid[row][column] == 1:
                    color = WHITE
                if grid[row][column] == 0:
                    color = BLACK

                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])

        pygame.display.flip()

    count = 0
    travelingGrid = newgrid
    hscore = [float("inf")] * (101 * 101)
    gscore = []
    current_location = start

    update_surrounding(travelingGrid, grid, current_location)

    [truepath, gscore, hscore] = adapta_star_search_G(start, target, travelingGrid, hscore)
    if truepath is False:
        print
        "Failed to find path"
        exit()
    truepath.reverse()
    # for i in truepath:
    #    hscore[i.getcellnum()] = gethuristic(start, target) - gscore[i.getcellnum()]
    #print (truepath)
    current_location = truepath[count]
    current_location.setagentpath(1)
    finalpath = [current_location]
    if current_location is target:
        return finalpath
    count += 1

    current_location = truepath[count]
    # showmaze(travelingGrid)

    while current_location is not target:

        if showdisplay:
            show_new_maze(grid, travelingGrid, screen, start, target)
        # print current_location
        # print target
        update_surrounding(travelingGrid, grid, current_location)

        finalpath.append(current_location)
        current_location.setagentpath(1)
        if truepath[count + 1].getblockstatus() == 0:
            reset_projected_path(truepath)
            [truepath, gscore, hscore] = adapta_star_search_G(current_location, target, travelingGrid, hscore)
            if truepath is False:
                print ("Failed to find path")
                pygame.quit()
                exit()
            # printfinalpath(truepath)

            truepath.reverse()
            # for i in truepath:
            #   hscore[i.getcellnum()]=gethuristic(start,target)-gscore[i.getcellnum()]

            count = 0
        count += 1
        current_location = truepath[count]
    if current_location is target:
        finalpath.append(current_location)
        current_location.setagentpath(1)
    # print grid
    #printfinalpath(finalpath)
    #print("fin fin fin path")

    fpath = create_final_path(finalpath)
    printfinalactualpath(fpath)
    #showmaze(travelingGrid)
   # print(travelingGrid[2][100].getagentpath())
    #print(travelingGrid[1][100].getagentpath())
    #show_new_maze(grid, travelingGrid, screen, start, target)
    #pygame.display.flip()
    while showdisplay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showdisplay = False
        show_new_maze(grid, travelingGrid, screen, start, target)


# print printfinalpath(create_final_path(finalpath))
##compute()
def adapta_star_search_G(intital, goal, grid,hscore):

    openlist=[]
    closedlist=[]
    hscor=hscore
    tree_list=[None]*(101*101)
    gscore=[float("inf")]*(101*101)
    fscore = [float("inf")] * (101 * 101)
    gscore[intital.getcellnum()]=0
    fscore[intital.getcellnum()]=get_new_hscore(intital,goal,hscor)
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    #neighbors = [(1,0)]
    heapify(openlist)
    heappush(openlist, (gethuristic(intital,goal),intital))
    tempcell=None
    while openlist:
        current_cell=heappop(openlist)
        #print current_cell[0]
        #print openlist
        if openlist:
            #tempcell=heappop(openlist)

            tempcell
            templist = []
            glist = []
            heappush(templist, current_cell)

            #### BIG G tie breaker stuff
            while openlist:
                tempcell = heappop(openlist)

                if tempcell[0] > current_cell[0]:
                    heappush(openlist, tempcell)
                    break
                else:
                    heappush(templist, tempcell)

            while templist:
                templist_temp = heappop(templist)
                heappush(glist, (gscore[templist_temp[1].getcellnum()], templist_temp[1]))

            highestg = None
            gcount = 0
            for g in glist:
                if highestg is None:
                    highestg = 0


                elif glist[highestg][0] < g[0]:
                    highestg = gcount
                gcount += 1

            current_cell = glist[highestg]
            while glist:
                pushback = heappop(glist)

                if pushback[1] is not current_cell[1]:
                    heappush(openlist, (fscore[pushback[1].getcellnum()], pushback[1]))

            ###END BIG G stuff
            #if tempcell[0]== current_cell[0]:

            #    if gscore[current_cell[1].getcellnum()]>= gscore[tempcell[1].getcellnum()]:
            #        heappush(openlist, tempcell)
            #    else:
            #        heappush(openlist,current_cell)
            #        current_cell = tempcell
            #else:
            #    heappush(openlist, tempcell)

        current_cell = current_cell[1]

        if current_cell == goal:
          #  print "target foundbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
            path_cell=current_cell
            #print path_cell
            #print goal
            #print tree_list[goal.getcellnum()]
            path=[]
            path.append(path_cell)
            path_cell.setprojectedpath(1)

            hscore[path_cell.getcellnum()]=gscore[goal.getcellnum()]-gscore[path_cell.getcellnum()]
           # print path

            while tree_list[path_cell.getcellnum()] in tree_list:
                if tree_list[path_cell.getcellnum()] is None:
                    return [path,gscore,hscore]
                path.append(tree_list[path_cell.getcellnum()])
                path_cell.setprojectedpath(1)
                hscore[path_cell.getcellnum()] = gscore[goal.getcellnum()] - gscore[path_cell.getcellnum()]
                #print path
                #print path
                path_cell=tree_list[path_cell.getcellnum()]
                if path_cell is None:
                    return [path,gscore,hscore]
            return [path,gscore,hscore]
        closedlist.append(current_cell)
        #print closedlist
        for x , y in neighbors:

            #print fscore[current_cell[1].getcellnum()]
            if (current_cell.getx() + x) <= -1 or (current_cell.getx() + x) >= 101 or (current_cell.gety() + y) <= -1 or (
                    current_cell.gety() + y) >= 101:
                continue
            temp = grid[current_cell.getx() + x][current_cell.gety() + y]
            #if temp ==goal:
            #    print "found the goal..."
             #   if temp.getblockstatus()==0:
             #       print temp.getx()
             #       print temp.gety()
             #       print temp.getblockstatus()
             #       return False

                #heappush(openlist,(0,temp))
                #tree_list[temp.getcellnum()]=current_cell[1]

                #fscore[temp.getcellnum()]=gscore[temp.getcellnum()]+gethuristic(temp,goal)
               # continue
            closed_test=False
            for t in closedlist:
                if t ==temp:
                    closed_test= True
                    #print "found it"


            if closed_test == True:
                #print "is in closed list"
                continue
            if temp.getblockstatus() == 0:
               # print  " blocked"
                continue
            test = False
            for s in openlist:
                if temp == s[1]:
                    test = True
            if test is True:
                continue
            # print "pushees"
            heappush(openlist, (gscore[current_cell.getcellnum()] + 1 + get_new_hscore(temp, goal,hscor), temp))
            temp_g_score=gscore[current_cell.getcellnum()]+1
            if temp_g_score >= gscore[temp.getcellnum()]:
                continue
            if temp_g_score < gscore[temp.getcellnum()]:
                tree_list[temp.getcellnum()]=current_cell
                gscore[temp.getcellnum()]=temp_g_score
                fscore[temp.getcellnum()]=gscore[temp.getcellnum()]+get_new_hscore(temp,goal,hscor)
    return False

gridnumber=39
gridtemp=np.load(os.getcwd()+"/mzs/grid"+str(gridnumber)+".npy")
newgrid=[]
creategrid(newgrid)
WIDTH = 7
HEIGHT = 7
MARGIN= 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
BROWN=(128,0,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
ORANGE=(255,165,0)
#shows loaded maze
def showmaze(grid2):

    pygame.init()
    WINDOW_SIZE = [2048, 2048]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    done = False
    while not done:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill(RED)
        for row in range(101):
            for column in range(101):
                color = BLACK
                if grid2[row][column]== 1:
                    color = WHITE
                if grid2[row][column]== 0:
                    color = BLACK
                    #grid2[row][column].setpath(1)

                #if row==0 or column ==0 or row==100 or column==100:
                    #color=
                #print grid2[row][column]
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
        pygame.display.flip()
    pygame.quit()
#print newgrid[100][0].getblockstatus()
#showmaze(newgrid)
#start=datetime.now()
#adaptive_a_astar(newgrid[0][0],newgrid[36][0],gridtemp,newgrid)
#print datetime.now()-start






