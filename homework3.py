import numpy as np
import math

def findNeighbours(currentNodeY, currentNodeX, ySize, xSize):
    neighbours = []
    for y in range(currentNodeY - 1, currentNodeY + 2):
            if(0 <= y and y < ySize):
                for x in range(currentNodeX - 1, currentNodeX + 2):
                    if(0 <= x and x < xSize):
                        if(y == currentNodeY and x == currentNodeX):
                            continue
                        #find new adjacent node
                        else:
                            neighbours.append([y, x])
    return neighbours

def totalCost(algorithm, nx, ny, sitex, sitey, currentNodeX, currentNodeY, mudLevel, heightChange):
    cost = 0
    # admissible heuristic
    if algorithm == "A*":
        cost += math.hypot(sitex - nx, sitey - ny)
    if(nx == currentNodeX or ny ==currentNodeY):
        cost += 10
    else:
        cost += 14
    cost += mudLevel
    cost += heightChange
    return cost
    
def output(nextPath, lastSite, fail):
    outputStr = ""
    f = open("output.txt", "a")
    if fail == 1:
        if lastSite == 1:
            outputStr = "FAIL"
        else:
            outputStr = "FAIL\n"
    else:
        for position in nextPath:
            if lastSite == 1:
                if position == nextPath[-1]:
                    outputStr += str(position[0]) + "," + str(position[1])
                else:
                    outputStr += str(position[0]) + "," + str(position[1])+" "
            else:
                if position == nextPath[-1]:
                    outputStr += str(position[0]) + "," + str(position[1])+ "\n"
                else:
                    outputStr += str(position[0]) + "," + str(position[1])+" "
    f.write(outputStr)
    f.close()

def BFS(startPoint, maxHeight, site, roadMap, lastSite):
    queue = []
    #Keep all the visited nodes in the list.
    visited = np.zeros([roadMap.shape[0], roadMap.shape[1]], dtype=np.int32)
    queue.append([startPoint])
    xSize = roadMap.shape[1]
    ySize = roadMap.shape[0]
    #Start BFS
    while(len(queue) > 0):
        path = queue.pop(0)
        currentNodeX = path[-1][0]
        currentNodeY = path[-1][1]
        visited[currentNodeY][currentNodeX] = 1
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
                #check if the new node is a rock
                if((roadMap[y][x] < 0 and abs(currentHeight - roadMap[y][x]) <= maxHeight) or (roadMap[y][x] >= 0 and abs(currentHeight) <= maxHeight)):
                    nextPath = path.copy()
                    nextPath.append([x, y])
                    queue.append(nextPath)
                    visited[y][x] = 1
                    if(x == site[0] and y == site[1]):
                        output(nextPath, lastSite, 0)
                        print("Shortest path = ", nextPath)
                        return
    
    output([], lastSite, 1)
    print("Shortest path: FAIL")
    return

def Asearch(algorithm, startPoint, maxHeight, site, roadMap, lastSite):
    pathLength = 0
    queue = []
    #Keep all the visited nodes in the list.
    visited = np.zeros([roadMap.shape[0], roadMap.shape[1]], dtype=np.int32)
    queue.append([pathLength, startPoint])
    xSize = roadMap.shape[1]
    ySize = roadMap.shape[0]
    #Start A*
    while(len(queue) > 0):
        path = queue[0]
        currentNodeX = path[-1][0]
        currentNodeY = path[-1][1]
        queue[-1], queue[0] = queue[0], queue[-1]
        queue.pop(-1)
        index = 0
        while (index * 2 + 1 < len(queue)):
            if index * 2 + 2 < len(queue):
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
                left = index * 2 + 1
                if queue[index][0] > queue[left][0]:
                    queue[index], queue[left] = queue[left], queue[index]
                    index = left
                else:
                    break

        if(currentNodeX == site[0] and currentNodeY == site[1]):
            path.pop(0)
            output(path, lastSite, 0)
            print("Shortest path = ", path)
            return
        visited[currentNodeY][currentNodeX] = 1
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
                #check if the new node is a rock
                if((roadMap[y][x] < 0 and abs(currentHeight - roadMap[y][x]) <= maxHeight) or (roadMap[y][x] >= 0 and abs(currentHeight) <= maxHeight)):
                    nextPath = path.copy()
                    nextPath.append([x, y])

                    if algorithm == "UCS":
                        nextPath[0] += totalCost(algorithm, x, y, 0, 0, currentNodeX, currentNodeY, 0, 0)
                    elif algorithm == "A*":
                        if (roadMap[y][x] >= 0):
                            #mud and no rock
                            mudLevel = roadMap[y][x]
                            heightChange = abs(currentHeight)
                        else:
                            #rock
                            mudLevel = 0
                            heightChange = abs(currentHeight - roadMap[y][x])
                        nextPath[0] += totalCost(algorithm, x, y, site[0], site[1], currentNodeX, currentNodeY, mudLevel, heightChange)
                    elif algorithm == "A*check":
                        if (roadMap[y][x] >= 0):
                            #mud and no rock
                            mudLevel = roadMap[y][x]
                            heightChange = abs(currentHeight)
                        else:
                            #rock
                            mudLevel = 0
                            heightChange = abs(currentHeight - roadMap[y][x])
                        nextPath[0] += totalCost(algorithm, x, y, 0, 0, currentNodeX, currentNodeY, mudLevel, heightChange)
                    #insert this path to queue sorted by pathlength
                    queue.append(nextPath)
                    index = len(queue)
                    while ((index // 2 ) > 0) :
                        if nextPath[0] < queue[index // 2 - 1][0]:

                            queue[index - 1], queue[index // 2 - 1] = queue[index // 2 - 1 ], queue[index - 1]
                            index = index // 2
                        else:
                            break
    output([], lastSite, 1)
    print("Shortest path: FAIL")      
    return

#read input file
lineNum = 0
currentrow = 0
inputFile = open("input.txt", "r")
outputFile = open("output.txt", "w")
for line in inputFile:
    lineNum += 1 
    if lineNum == 1:
        algorithm = line.strip("\n")
    elif lineNum == 2:
        tokens = list(map(int, line.split()))
        row = tokens[1]
        roadMap = np.empty((tokens[1], tokens[0]), dtype=np.int32)
    elif lineNum == 3:
        startPoint = list(map(int, line.split()))
    elif lineNum == 4:
        maxHeight = int(line)
    elif lineNum == 5:
        numOfSite = int(line)
        siteList = []
    elif lineNum <= 5+numOfSite:
        siteList.append(list(map(int, line.split())))
    else:
        roadMap[currentrow] = list(map(int, line.split()))
        currentrow += 1

#BFS
if algorithm == "BFS":
    for site in siteList:
        if site == siteList[-1]:
            BFS(startPoint, maxHeight, site, roadMap, 1)
        else:
            BFS(startPoint, maxHeight, site, roadMap, 0)
elif algorithm == "A*" or algorithm == "UCS" or algorithm == "A*check":
    for site in siteList:
        if site == siteList[-1]:
            Asearch(algorithm, startPoint, maxHeight, site, roadMap, 1)
        else:
            Asearch(algorithm, startPoint, maxHeight, site, roadMap, 0)