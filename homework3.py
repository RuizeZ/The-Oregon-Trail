import numpy as np
import math
def findNeighbours(currentNodeY, currentNodeX, ySize, xSize):
    neighbours = []
    for y in range(currentNodeY - 1, currentNodeY + 2):
            ##print("y: %d" %y)
            if(0 <= y and y < ySize):
                for x in range(currentNodeX - 1, currentNodeX + 2):
                    ##print("x: %d" %x)
                    if(0 <= x and x < xSize):
                        if(y == currentNodeY and x == currentNodeX):
                            continue
                        #find new adjacent node
                        else:
                            neighbours.append([y, x])
    return neighbours

def totalCost(nx, ny, sitex, sitey, currentNodeX, currentNodeY, mudLevel, heightChange):
    cost = 0
    # admissible heuristic
    cost += math.hypot(sitex - nx, sitey - ny)
    if(nx == currentNodeX or ny ==currentNodeY):
        cost += 10
    else:
        cost += 14
    cost += mudLevel
    cost += heightChange
    return cost
    

def BFS(startPoint, maxHeight, site, roadMap):
    queue = []
    #Keep all the visited nodes in the list.
    visited = np.zeros([roadMap.shape[0], roadMap.shape[1]], dtype=np.int32)
    queue.append([startPoint])
    ##print("queue: ",queue)
    xSize = roadMap.shape[1]
    ySize = roadMap.shape[0]
    if(startPoint[0] == site[0] and startPoint[1] == site[1]):
        print("Shortest path:", site)
        return 
    #Start BFS
    while(len(queue) > 0):
        path = queue.pop(0)
        ##print("path ", path)
        currentNodeX = path[-1][0]
        currentNodeY = path[-1][1]
        ##print("curentNode: %d %d" %(currentNodeX,currentNodeY))
        visited[currentNodeY][currentNodeX] = 1
        ##print("visited:")
        ##print(visited)
        """
        y-axis = currentNodeY
        x-axis = currentNodeX
        """
        # neighbours[] contains all 8 adjacent nodes
        neighbours = findNeighbours(currentNodeY, currentNodeX, ySize, xSize)
        #set the current height if the node is a rock
        if(roadMap[currentNodeY][currentNodeX] < 0):
            currentHeight = roadMap[currentNodeY][currentNodeX]
        else:
            currentHeight = 0
        #check if the node has been visited
        for neighbour in neighbours:
            y = neighbour[0]
            x = neighbour[1]
            if(visited[y][x] != 1):
                ##print("nextNode: %d,%d" %(x, y))
                #check if the new node is a rock
                if((roadMap[y][x] < 0 and abs(currentHeight - roadMap[y][x]) <= maxHeight) or (roadMap[y][x] >= 0 and abs(currentHeight) <= maxHeight)):
                    ##print("path ", path)
                    nextPath = path.copy()
                    ##print("nextPath ", nextPath)
                    nextPath.append([x, y])
                    ##print("nextPath.append([x, y]) ", nextPath)
                    queue.append(nextPath)
                    ##print("queue.append(nextPath) ",queue)
                    visited[y][x] = 1
                    ##print("visited:")
                    ##print(visited)

                    if(x == site[0] and y == site[1]):
                        print("Shortest path = ", nextPath)
                        return
    print("Shortest path: FAIL")      
    return

def UCS(startPoint, maxHeight, site, roadMap):
    pathLength = 0
    queue = []
    #Keep all the visited nodes in the list.
    visited = np.zeros([roadMap.shape[0], roadMap.shape[1]], dtype=np.int32)
    queue.append([pathLength, startPoint])
    #print("queue: ",queue)
    xSize = roadMap.shape[1]
    ySize = roadMap.shape[0]
    if(startPoint[0] == site[0] and startPoint[1] == site[1]):
        print("Shortest path:", site)
        return 
    #Start UCS
    while(len(queue) > 0):
        path = queue[0]
        #print("queue ", queue)
        currentNodeX = path[-1][0]
        currentNodeY = path[-1][1]
        queue[-1], queue[0] = queue[0], queue[-1]
        queue.pop(-1)
        index = 0
        while (index * 2 + 1 < len(queue)):
            #print("in while")
            if index * 2 + 2 < len(queue):
                #print("in if")
                left = index * 2 + 1
                right = index * 2 + 2
                if queue[index][0] >= max(queue[left][0], queue[right][0]):
                    if queue[left][0] == min(queue[left][0], queue[right][0]):
                        nextIndex = left
                    else:
                        nextIndex = right
                    queue[index], queue[nextIndex] = queue[nextIndex], queue[index]
                    index = nextIndex
                else:
                    break
            else:
                #print("in else")
                left = index * 2 + 1
                if queue[index][0] > queue[left][0]:
                    queue[index], queue[left] = queue[left], queue[index]
                    index = left
                else:
                    break

        if(currentNodeX == site[0] and currentNodeY == site[1]):
            print("Shortest path = ", path)
            return
        ##print("curentNode: %d %d" %(currentNodeX,currentNodeY))
        visited[currentNodeY][currentNodeX] = 1
        ##print("visited:")
        ##print(visited)
        """
        y-axis = currentNodeY
        x-axis = currentNodeX
        """
        # neighbours[] contains all 8 adjacent nodes
        neighbours = findNeighbours(currentNodeY, currentNodeX, ySize, xSize)
        #set the current height if the node is a rock
        if(roadMap[currentNodeY][currentNodeX] < 0):
            currentHeight = roadMap[currentNodeY][currentNodeX]
        else:
            currentHeight = 0
        for neighbour in neighbours:
            y = neighbour[0]
            x = neighbour[1]
            #check if the node has been visited
            if(visited[y][x] != 1):
                ##print("nextNode: %d,%d" %(x, y))
                #check if the new node is a rock
                if((roadMap[y][x] < 0 and abs(currentHeight - roadMap[y][x]) <= maxHeight) or (roadMap[y][x] >= 0 and abs(currentHeight) <= maxHeight)):
                    ##print("path ", path)
                    nextPath = path.copy()
                    ##print("nextPath ", nextPath)
                    nextPath.append([x, y])

                    if(x == currentNodeX or y ==currentNodeY):
                        nextPath[0] += 10
                    else:
                        nextPath[0] += 14
                    
                    
                    
                    
                    #print("nextPath.append([x, y]) ", nextPath)
                    #insert this path to queue sorted by pathlength
                    queue.append(nextPath)
                    #print("queue.append(nextPath) ",queue)
                    index = len(queue)
                    #print("index: ", index)
                    while ((index // 2 ) > 0) :
                        #print("index // 2: ", index // 2)
                        if nextPath[0] < queue[index // 2 - 1][0]:

                            queue[index - 1], queue[index // 2 - 1] = queue[index // 2 - 1 ], queue[index - 1]
                            index = index // 2
                        else:
                            break

                    #print("sorted queue",queue)
    print("Shortest path: FAIL")      
    return

def Asearch(algorithm, startPoint, maxHeight, site, roadMap):
    pathLength = 0
    queue = []
    #Keep all the visited nodes in the list.
    visited = np.zeros([roadMap.shape[0], roadMap.shape[1]], dtype=np.int32)
    queue.append([pathLength, startPoint])
    #print("queue: ",queue)
    xSize = roadMap.shape[1]
    ySize = roadMap.shape[0]
    if(startPoint[0] == site[0] and startPoint[1] == site[1]):
        print("Shortest path:", site)
        return 
    #Start A*
    while(len(queue) > 0):
        path = queue[0]
        #print("queue ", queue)
        currentNodeX = path[-1][0]
        currentNodeY = path[-1][1]
        queue[-1], queue[0] = queue[0], queue[-1]
        queue.pop(-1)
        index = 0
        while (index * 2 + 1 < len(queue)):
            #print("in while")
            if index * 2 + 2 < len(queue):
                #print("in if")
                left = index * 2 + 1
                right = index * 2 + 2
                if queue[index][0] > queue[left][0] and queue[index][0] <= queue[right][0]:
                    queue[index], queue[left] = queue[left], queue[index]
                    nextIndex = left

                elif queue[index][0] > queue[right][0] and queue[index][0] <= queue[left][0]:
                    queue[index], queue[right] = queue[right], queue[index]
                    nextIndex = right
                    
                elif queue[index][0] > max(queue[left][0], queue[right][0]):
                    if queue[left][0] == min(queue[left][0], queue[right][0]):
                        nextIndex = left
                    else:
                        nextIndex = right
                    queue[index], queue[nextIndex] = queue[nextIndex], queue[index]

                else:
                    break
                index = nextIndex
            else:
                #print("in else")
                left = index * 2 + 1
                if queue[index][0] > queue[left][0]:
                    queue[index], queue[left] = queue[left], queue[index]
                    index = left
                else:
                    break

        if(currentNodeX == site[0] and currentNodeY == site[1]):
            print("Shortest path = ", path)
            return
        ##print("curentNode: %d %d" %(currentNodeX,currentNodeY))
        visited[currentNodeY][currentNodeX] = 1
        ##print("visited:")
        ##print(visited)
        """
        y-axis = currentNodeY
        x-axis = currentNodeX
        """
        # neighbours[] contains all 8 adjacent nodes
        neighbours = findNeighbours(currentNodeY, currentNodeX, ySize, xSize)
        #set the current height if the node is a rock
        if(roadMap[currentNodeY][currentNodeX] < 0):
            currentHeight = roadMap[currentNodeY][currentNodeX]
        else:
            currentHeight = 0
        for neighbour in neighbours:
            y = neighbour[0]
            x = neighbour[1]
            #check if the node has been visited
            if(visited[y][x] != 1):
                ##print("nextNode: %d,%d" %(x, y))
                #check if the new node is a rock
                if((roadMap[y][x] < 0 and abs(currentHeight - roadMap[y][x]) <= maxHeight) or (roadMap[y][x] >= 0 and abs(currentHeight) <= maxHeight)):
                    ##print("path ", path)
                    nextPath = path.copy()
                    ##print("nextPath ", nextPath)
                    nextPath.append([x, y])

                    if algorithm == "UCS":
                        nextPath[0] += totalCost(0, 0, 0, 0, currentNodeX, currentNodeY, 0, 0)
                    elif algorithm == "A*":
                        if (roadMap[y][x] >= 0):
                            #mud and no rock
                            mudLevel = roadMap[y][x]
                            heightChange = abs(currentHeight)
                        else:
                            #rock
                            mudLevel = 0
                            heightChange = abs(currentHeight - roadMap[y][x])
                        nextPath[0] += totalCost(x, y, site[0], site[1], currentNodeX, currentNodeY, mudLevel, heightChange)
                    
                    
                    
                    
                    # if(x == currentNodeX or y ==currentNodeY):
                    #     nextPath[0] += 10
                    # else:
                    #     nextPath[0] += 14
                    ##print("nextPath.append([x, y]) ", nextPath)

                    #insert this path to queue sorted by pathlength
                    queue.append(nextPath)
                    #print("queue.append(nextPath) ",queue)
                    index = len(queue)
                    #print("index: ", index)
                    while ((index // 2 ) > 0) :
                        #print("index // 2: ", index // 2)
                        if nextPath[0] < queue[index // 2 - 1][0]:

                            queue[index - 1], queue[index // 2 - 1] = queue[index // 2 - 1 ], queue[index - 1]
                            index = index // 2
                        else:
                            break

                    #print("sorted queue",queue)
    print("Shortest path: FAIL")      
    return


#read input file
lineNum = 0
currentrow = 0
inputFile = open("input.txt", "r")
for line in inputFile:
    lineNum += 1 
    if lineNum == 1:
        algorithm = line.strip("\n")
        ##print("algorithm:", algorithm)
    elif lineNum == 2:
        tokens = list(map(int, line.split()))
        row = tokens[1]
        roadMap = np.empty((tokens[1], tokens[0]), dtype=np.int32)
    elif lineNum == 3:
        startPoint = list(map(int, line.split()))
        ##print("startPoint:", startPoint)
    elif lineNum == 4:
        maxHeight = int(line)
        ##print("maxHeight:", maxHeight)
    elif lineNum == 5:
        numOfSite = int(line)
        ##print("numOfSite:", numOfSite)
        siteList = []
    elif lineNum <= 5+numOfSite:
        siteList.append(list(map(int, line.split())))
    else:
        roadMap[currentrow] = list(map(int, line.split()))
        currentrow += 1
##print("siteList:", siteList)
##print("roadMap:", roadMap)

#BFS
if algorithm == "BFS":
    ##print("in bfs")
    for site in siteList:
        BFS(startPoint, maxHeight, site, roadMap)
# elif algorithm == "UCS":
#     #print("in bfs")
#     for site in siteList:
#         UCS(startPoint, maxHeight, site, roadMap)
elif algorithm == "A*" or algorithm == "UCS":
    for site in siteList:
        Asearch(algorithm, startPoint, maxHeight, site, roadMap)

