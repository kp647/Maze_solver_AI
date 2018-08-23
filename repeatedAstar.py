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
##returns h value
def gethuristic(cellA,cellB):
    distance= abs(cellB.getx()-cellA.getx())+abs(cellB.gety()-cellA.gety())
    return distance
#prints final path
def printfinalpath(path):
    for i in path:
        print str(i.getx()) + "   " + str(i.gety())


#prints final path and sets node atribute path to =1
def printfinalactualpath(path):
    for i in path:
        print str(i.getx()) + "   " + str(i.gety())
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

##updates grid of agents surrouding block cells it encounterd
def update_surrounding(travelingGrid,grid,cell):
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if grid[cell.getx()][cell.gety()] == 0:
        travelingGrid[cell.getx()][cell.gety()].setblockstatus(0)
    for x, y in neighbors:
        if (cell.getx() + x) <= -1 or (cell.getx() + x) >= 101 or (
                cell.gety() + y) <= -1 or (
                cell.gety() + y) >= 101:
            continue
        if grid[cell.getx()+x][cell.gety()+y]==0:
            travelingGrid[cell.getx()+x][cell.gety()+y].setblockstatus(0)

#creates grid
def creategrid(grid):
    counter = 0
    for row in range(101):
        grid.append([])


        for column in range(101):
            grid[row].append(Node(1,counter,row,column,0))


            counter+=1

#reverses list
def reverse_list(lis):
    templist=[]
    for i in list:
        templist.append(lis.pop())
    return templist

#shows the maze visual while agent is moving
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
            if travelingGrid[row][column].getprojectedpath() == 1 and travelingGrid[row][column].getagentpath() == 1:
                color = BROWN
            elif travelingGrid[row][column].getprojectedpath() == 1:
                color = BLUE
            if travelingGrid[row][column].getagentpath() == 1:
                color = BROWN
            if travelingGrid[row][column].ispath() == 1:
                color = GREEN
            if travelingGrid[row][column]== start:
                color=YELLOW
            if travelingGrid[row][column]== target:
                color=ORANGE
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

#repeated foward main() with smaller g values
def repeated_foward_a_astar_littleg(start, target, grid,newgrid):
    #showdisplay can turn the visual on or off
    showdisplay= True
    if showdisplay is True:
        pygame.init()
        WINDOW_SIZE = [2048, 2048]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        for row in range(101):
            for column in range(101):
                color = BLACK
                if grid[row][column]== 1:
                    color = WHITE
                if grid[row][column]== 0:
                    color = BLACK

                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        pygame.display.flip()



    count=0
    travelingGrid=newgrid
    tree_pointer=[None]*(101*101)
    current_location=start
    update_surrounding(travelingGrid,grid,current_location)
    if current_location.getblockstatus()==0:
        print "Starting cell is blocked"
        exit()
    [truepath,tree_pointer]=a_star_search_littleg(start,target,travelingGrid,tree_pointer)

    if truepath is False:
        print "Target is a Blocked Cell"
        exit()
    truepath.reverse()
    #print truepath
    current_location=truepath[count]
    current_location.setagentpath(1)
    finalpath=[current_location]
    if current_location is target:
        return finalpath
    count+=1

    current_location=truepath[count]
    #showmaze(travelingGrid)

    while current_location is not target:

        if showdisplay:
            show_new_maze(grid,travelingGrid,screen,start,target)





       # print current_location
        #print target
        update_surrounding(travelingGrid,grid,current_location)

        finalpath.append(current_location)
        current_location.setagentpath(1)
        if truepath[count+1].getblockstatus()== 0:
            reset_projected_path(truepath)
            [truepath,tree_pointer] = a_star_search_littleg(current_location, target, travelingGrid,tree_pointer)
            if truepath is False:
                print "Target is a Blocked Path"
                pygame.quit()
                exit()
            #printfinalpath(truepath)

            truepath.reverse()
            count=0
        count+=1
        current_location=truepath[count]
        current_location.setagentpath(1)
    if current_location is target:
        finalpath.append(current_location)
    #print grid
    current_location=truepath[count]
    current_location.setagentpath(1)
    #printfinalpath(finalpath)
    #print "fin fin fin path"

    fpath= create_final_path(finalpath)
    printfinalactualpath(fpath)
    while showdisplay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showdisplay = False
        show_new_maze(grid,travelingGrid,screen,start,target)

#repeated foward main() larger G
def repeated_foward_a_astar_G(start, target, grid,newgrid):
    # showdisplay can turn the visual on or off
    showdisplay= True
    if showdisplay is True:
        pygame.init()
        WINDOW_SIZE = [2048, 2048]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        for row in range(101):
            for column in range(101):
                color = BLACK
                if grid[row][column]== 1:
                    color = WHITE
                if grid[row][column]== 0:
                    color = BLACK

                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        pygame.display.flip()



    count=0
    travelingGrid=newgrid
    tree_pointer=[None]*(101*101)
    current_location=start
    update_surrounding(travelingGrid,grid,current_location)
    if current_location.getblockstatus()==0:
        print "Starting cell is blocked"
        exit()
    [truepath,tree_pointer]=a_star_search_G(start,target,travelingGrid,tree_pointer)

    if truepath is False:
        print "Target is a Blocked Cell"
        exit()
    truepath.reverse()
    #print truepath
    current_location=truepath[count]
    current_location.setagentpath(1)
    finalpath=[current_location]
    if current_location is target:
        return finalpath
    count+=1

    current_location=truepath[count]
    #showmaze(travelingGrid)

    while current_location is not target:

        if showdisplay:
            show_new_maze(grid,travelingGrid,screen,start,target)





       # print current_location
        #print target
        update_surrounding(travelingGrid,grid,current_location)

        finalpath.append(current_location)
        current_location.setagentpath(1)
        if truepath[count+1].getblockstatus()== 0:
            reset_projected_path(truepath)
            [truepath,tree_pointer] = a_star_search_G(current_location, target, travelingGrid,tree_pointer)
            if truepath is False:
                print "Target is a Blocked Path"
                pygame.quit()
                exit()
            #printfinalpath(truepath)

            truepath.reverse()
            count=0
        count+=1
        current_location=truepath[count]
        current_location.setagentpath(1)
        pygame.display.get_surface()
    if current_location is target:
        finalpath.append(current_location)
    #print grid
    current_location=truepath[count]
    current_location.setagentpath(1)
    fpath= create_final_path(finalpath)
    printfinalactualpath(fpath)
    #show_new_maze(grid,travelingGrid,screen,start,target)

    while showdisplay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showdisplay = False
        show_new_maze(grid,travelingGrid,screen,start,target)

#repeated backward larger g main()
def repeated_backward_a_astar_G(start, target, grid,newgrid):
    # showdisplay can turn the visual on or off
    showdisplay= True
    if showdisplay is True:
        pygame.init()
        WINDOW_SIZE = [2048, 2048]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        for row in range(101):
            for column in range(101):
                color = BLACK
                if grid[row][column]== 1:
                    color = WHITE
                if grid[row][column]== 0:
                    color = BLACK

                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        pygame.display.flip()



    count=0
    travelingGrid=newgrid
    tree_pointer=[None]*(101*101)
    current_location=target

    update_surrounding(travelingGrid,grid,current_location)
    if current_location.getblockstatus()==0:
        print "Starting cell is blocked"
        exit()
    if target.getblockstatus()==0:
        print "Target is blocked"
        exit()

    [truepath,tree_pointer]=a_star_search_G(target,start,travelingGrid,tree_pointer)

    if truepath is False:
        print "Target is a Blocked Cell"
        exit()
    truepath.reverse()
    #print truepath
    current_location=truepath[count]
    current_location.setagentpath(1)
    finalpath=[current_location]
    if current_location is start:
        return finalpath
    count+=1

    current_location=truepath[count]
    #showmaze(travelingGrid)

    while current_location is not start:

        if showdisplay:
            show_new_maze(grid,travelingGrid,screen,start,target)





       # print current_location
        #print target
        update_surrounding(travelingGrid,grid,current_location)

        finalpath.append(current_location)
        current_location.setagentpath(1)
        if truepath[count+1].getblockstatus()== 0:
            reset_projected_path(truepath)
            [truepath,tree_pointer] = a_star_search_G(current_location, start, travelingGrid,tree_pointer)
            if truepath is False:
                print "Target is a Blocked Path"
                pygame.quit()
                exit()
            #printfinalpath(truepath)

            truepath.reverse()
            count=0
        count+=1
        current_location=truepath[count]
        current_location.setagentpath(1)
    if current_location is target:
        finalpath.append(current_location)
    #print grid
    current_location=truepath[count]
    current_location.setagentpath(1)
    #printfinalpath(finalpath)
    #print "fin fin fin path"

    fpath= create_final_path(finalpath)
    printfinalactualpath(fpath)
    while showdisplay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showdisplay = False
        show_new_maze(grid,travelingGrid,screen,start,target)
   # print printfinalpath(create_final_path(finalpath))

#compute() a start smaller g score search
def a_star_search_littleg(intital, goal, grid,treepath):

    openlist=[]
    closedlist=[]
    a_tree_list=[None]*(101*101)
    gscore=[float("inf")]*(101*101)
    fscore = [float("inf")] * (101 * 101)
    gscore[intital.getcellnum()]=0
    fscore[intital.getcellnum()]=gethuristic(intital,goal)
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    #neighbors = [(1,0)]
    heapify(openlist)
    heappush(openlist,(gethuristic(intital,goal),intital))
    tempcell=None

    while openlist:

        current_cell=heappop(openlist)

        #print current_cell[0]
        #print openlist
        #### little G tie breaker stuff
        if openlist:
            tempcell
            templist=[]
            glist=[]
            heappush(templist,current_cell)

            while openlist:
                tempcell=heappop(openlist)


                if tempcell[0]>current_cell[0]:
                    heappush(openlist,tempcell)
                    break
                else:
                    heappush(templist,tempcell)

            while templist:
                templist_temp=heappop(templist)
                heappush(glist,(gscore[templist_temp[1].getcellnum()],templist_temp[1]))

            lowestg=None
            gcount=0
            for g in glist:
                if lowestg is None:
                    lowestg=0


                elif glist[lowestg][0]>g[0]:
                    lowestg=gcount
                gcount+=1

            current_cell=glist[lowestg]
            while glist:
                pushback=heappop(glist)

                if pushback[1] is not current_cell[1]:
                    heappush(openlist,(fscore[pushback[1].getcellnum()],pushback[1]))

        current_cell = current_cell[1]






       # print current_cell

        if current_cell == goal:
            #print "target found"
            path_cell=current_cell
            #print path_cell
            #print goal
            path=[]
            path.append(path_cell)
            path_cell.setprojectedpath(1)
           # print path

            while a_tree_list[path_cell.getcellnum()] in a_tree_list:
                #print path_cell
                if a_tree_list[path_cell.getcellnum()] is None:
                    return [path,a_tree_list]
                path.append(a_tree_list[path_cell.getcellnum()])
                #print path
                #print path
                path_cell=a_tree_list[path_cell.getcellnum()]
                path_cell.setprojectedpath(1)
                if path_cell is None:
                    return [path,a_tree_list]
            return [path,a_tree_list]
        closedlist.append(current_cell)
        #print closedlist
        for x , y in neighbors:

            #print fscore[current_cell[1].getcellnum()]
            if (current_cell.getx() + x) <= -1 or (current_cell.getx() + x) >= 101 or (current_cell.gety() + y) <= -1 or (
                    current_cell.gety() + y) >= 101:
                continue
            temp = grid[current_cell.getx() + x][current_cell.gety() + y]
            if temp ==goal and temp.getblockstatus()==0:
                return [False,False]
            #    print "found the goal..."
             #   if temp.getblockstatus()==0:
             #       print temp.getx()
             #       print temp.gety()
             #       print temp.getblockstatus()
             #       return False

                #heappush(openlist,(0,temp))

                #fscore[temp.getcellnum()]=gscore[temp.getcellnum()]+gethuristic(temp,goal)
               # continue
            closed_test=False
            for t in closedlist:
                if t ==temp:
                    closed_test= True
               #     #print "found it"


            if closed_test == True:
                #print "is in closed list"
                continue
           # if temp in closedlist:
            #    continue
            if temp.getblockstatus() == 0:
                #print  " blocked"
                continue
            test = False
            for s in openlist:
                if temp == s[1]:
                    test = True
            if test is True:
                continue
            #t1=(fscore[temp.getcellnum()],temp)
            #if t1 in openlist:
              #  continue
            # print "pushees"
            heappush(openlist, (gscore[current_cell.getcellnum()] + 1 + gethuristic(temp, goal), temp))
            temp_g_score=gscore[current_cell.getcellnum()]+1
            if temp_g_score >= gscore[temp.getcellnum()]:
                continue
            if temp_g_score < gscore[temp.getcellnum()]:
                a_tree_list[temp.getcellnum()]=current_cell
                gscore[temp.getcellnum()]=temp_g_score
                fscore[temp.getcellnum()]=gscore[temp.getcellnum()]+gethuristic(temp,goal)
    return False

#compute() a start larger g score search
def a_star_search_G(intital, goal, grid,treepath):

    openlist=[]
    closedlist=[]
    a_tree_list=[None]*(101*101)
    gscore=[float("inf")]*(101*101)
    fscore = [float("inf")] * (101 * 101)
    gscore[intital.getcellnum()]=0
    fscore[intital.getcellnum()]=gethuristic(intital,goal)
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    #neighbors = [(1,0)]
    heapify(openlist)
    heappush(openlist,(gethuristic(intital,goal),intital))
    tempcell=None
    while openlist:

        current_cell=heappop(openlist)

        #print current_cell[0]
        #print openlist
        #### BIG G tie breaker stuff
        if openlist:
            tempcell
            templist=[]
            glist=[]
            heappush(templist,current_cell)

            while openlist:
                tempcell=heappop(openlist)


                if tempcell[0]>current_cell[0]:
                    heappush(openlist,tempcell)
                    break
                else:
                    heappush(templist,tempcell)

            while templist:
                templist_temp=heappop(templist)
                heappush(glist,(gscore[templist_temp[1].getcellnum()],templist_temp[1]))

            highestg=None
            gcount=0
            for g in glist:
                if highestg is None:
                    highestg=0


                elif glist[highestg][0]<g[0]:
                    highestg=gcount
                gcount+=1

            current_cell=glist[highestg]
            while glist:
                pushback=heappop(glist)

                if pushback[1] is not current_cell[1]:
                    heappush(openlist,(fscore[pushback[1].getcellnum()],pushback[1]))








       # print current_cell
        current_cell=current_cell[1]

        if current_cell == goal:
            #print "target found"
            path_cell=current_cell
            #print path_cell
            #print goal
            path=[]
            path.append(path_cell)
            path_cell.setprojectedpath(1)
           # print path

            while a_tree_list[path_cell.getcellnum()] in a_tree_list:
                #print path_cell
                if a_tree_list[path_cell.getcellnum()] is None:
                    return [path,a_tree_list]
                path.append(a_tree_list[path_cell.getcellnum()])
                #print path
                #print path
                path_cell=a_tree_list[path_cell.getcellnum()]
                path_cell.setprojectedpath(1)
                if path_cell is None:
                    return [path,a_tree_list]
            return [path,a_tree_list]
        closedlist.append(current_cell)
        #print closedlist
        for x , y in neighbors:

            #print fscore[current_cell[1].getcellnum()]
            if (current_cell.getx() + x) <= -1 or (current_cell.getx() + x) >= 101 or (current_cell.gety() + y) <= -1 or (
                    current_cell.gety() + y) >= 101:
                continue
            temp = grid[current_cell.getx() + x][current_cell.gety() + y]
            if temp ==goal and temp.getblockstatus()==0:
                return [False,False]



            closed_test=False
            for t in closedlist:
                if t ==temp:
                    closed_test= True
               #     #print "found it"


            if closed_test == True:
                #print "is in closed list"
                continue
           # if temp in closedlist:
            #    continue
            if temp.getblockstatus() == 0:
                #print  " blocked"
                continue
            test = False
            for s in openlist:
                if temp == s[1]:
                    test = True
            if test is True:
                continue
            #t1=(fscore[temp.getcellnum()],temp)
            #if t1 in openlist:
              #  continue
            # print "pushees"
            heappush(openlist, (gscore[current_cell.getcellnum()] + 1 + gethuristic(temp, goal), temp))
            temp_g_score=gscore[current_cell.getcellnum()]+1
            if temp_g_score >= gscore[temp.getcellnum()]:
                continue
            if temp_g_score < gscore[temp.getcellnum()]:
                a_tree_list[temp.getcellnum()]=current_cell
                gscore[temp.getcellnum()]=temp_g_score
                fscore[temp.getcellnum()]=gscore[temp.getcellnum()]+gethuristic(temp,goal)
    return False


##selects which grid to load
gridnumber=1
#gets mzs folder that contains mazes from cur.direc
gridtemp=np.load(os.getcwd()+"/mzs/grid"+str(gridnumber)+".npy")##loads grid
newgrid=[]
creategrid(newgrid)##creates grid of 101*101 nodes
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

#*start=datetime.now()
#repeated_foward_a_astar_littleg(newgrid[0][0],newgrid[36][0],gridtemp,newgrid)
#print datetime.now()-start
#newgrid=[]
#creategrid(newgrid)
#start=datetime.now()
#repeated_foward_a_astar_G(newgrid[0][0],newgrid[36][0],gridtemp,newgrid)
#print datetime.now()-start
#newgrid=[]
#creategrid(newgrid)
#start=datetime.now()
#repeated_backward_a_astar_G(newgrid[0][0],newgrid[36][0],gridtemp,newgrid)
#print datetime.now()-start


