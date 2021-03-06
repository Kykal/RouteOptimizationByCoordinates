import numpy as np
import sys
import time
import math
import random as rand

#Declaring variables
nodes = []
route = []
routeCoords = []
nodesDistance = []
nodesNumbers = []
tempNodes = []
tempNumberNodes = []
possibleNodes = -1
totalDistance = 0
bestDistance = sys.float_info.max
tempInternStatus = []
actualTime = 0
timeLimit = 5.0 #seconds
timeLimitExceed = False

#Function to calculate Euclidean Distance
def Eu2D(x1, y1, x2, y2):
    return np.sqrt( (x1-x2)**2 + (y1-y2)**2 )

#Open the file we want to use
filename = "ulysses16"
tsp = open("TSP/"+filename+".tsp", "r")

#Jump lines to 'Dimension', save its dimension and jump to coordenates
for x in range(3):
    tsp.readline()
dimension = int( tsp.readline().split()[1] )
n = dimension-1
for x in range(2):
    tsp.readline()

#Save coordinates in a matrix called 'nodes' and assings the status of True to all nodes.
for i in range(0, dimension):
    x,y = tsp.readline().strip().split()[1:]
    nodes.append([float(x), float(y)])
status = [True for i in range(dimension)]

#Asks user where to start, save input as integer subtracting one. Saves initial coordinates as 'initCoords' and its coordinates.
print("\n%s file loaded." %filename)
initNumber = int( input("From 1 to %s\n\tWhere do you want to start?: " %dimension) ) - 1
print("Calculating, plase wait.\n")
initCoords = nodes[initNumber]
x1 = initCoords[0]
y1 = initCoords[1]

#Append variables to 'route' and 'routeCoords'.
route.append(initNumber+1)
routeCoords.append(initCoords)

#Algorithm timer execute
startTime = time.time()

#Nearest Neighbor with k-best method
for a in range(0, 3**dimension) :
    actualTime = time.time() - startTime
    if actualTime >= timeLimit :
        timeLimitExceed = True
        break
    route.clear()
    route.append(initNumber+1)
    nodesDistance.clear()
    nodesNumbers.clear()
    tempNodes.clear()
    tempNumberNodes.clear()
    possibleNodes = -1
    x1 = initCoords[0]
    y1 = initCoords[1]
    totalDistance = 0
    status = [True for i in range(dimension)]
    tempInternStatus.clear()
    for i in range( 0, dimension-1 ) :
        actualTime = time.time() - startTime
        if actualTime >= timeLimit :
            timeLimitExceed = True
            break
        minumumDistance = sys.float_info.max
        possibleNodes = -1
        nodesNumbers.clear()
        nodesDistance.clear()
        tempNodes.clear()
        tempNumberNodes.clear()

        for j in range( 0, dimension ) : #Obtain all euclidean distances
            actualTime = time.time() - startTime
            if actualTime >= timeLimit :
                timeLimitExceed = True
                break
            x2 = nodes[j][0]
            y2 = nodes[j][1]
            
            euclideanDistance = Eu2D(x1, y1, x2, y2 )
            nodesDistance.append(euclideanDistance)
            nodesNumbers.append(j)
        status[initNumber] = False
        tempInternStatus = status.copy()
        tempStatus = status.copy()

        if sum(tempStatus) > 0 :
            actualTime = time.time() - startTime
            if actualTime >= timeLimit :
                timeLimitExceed = True
                break
            for j in range(0, dimension) : #First kBest
                actualTime = time.time() - startTime
                if actualTime >= timeLimit :
                    timeLimitExceed = True
                    break
                if (tempInternStatus[j] == True) and (nodesDistance[j] < minumumDistance) :
                    minumumDistance = nodesDistance[j]
                    tempInternStatus[j] = False
                    tempNode = j
            tempStatus[tempNode] = False
            tempNodes.append(nodes[tempNode])
            tempNumberNodes.append(tempNode)
            tempInternStatus = tempStatus.copy()
            minumumDistance = sys.float_info.max
            possibleNodes += 1

        if sum(tempStatus) > 0 :
            actualTime = time.time() - startTime
            if actualTime >= timeLimit :
                timeLimitExceed = True
                break
            for j in range(0, dimension) : #Second kBest
                actualTime = time.time() - startTime
                if actualTime >= timeLimit :
                    timeLimitExceed = True
                    break
                if (tempInternStatus[j] == True) and (nodesDistance[j] < minumumDistance) :
                    minumumDistance = nodesDistance[j]
                    tempInternStatus[j] = False
                    tempNode = j
            tempStatus[tempNode] = False
            tempNodes.append(nodes[tempNode])
            tempNumberNodes.append(tempNode)
            tempInternStatus = tempStatus.copy()
            minumumDistance = sys.float_info.max
            possibleNodes += 1

        if sum(tempStatus) > 0 :
            actualTime = time.time() - startTime
            if actualTime >= timeLimit :
                timeLimitExceed = True
                break
            for j in range(0, dimension) : #Third kBest
                actualTime = time.time() - startTime
                if actualTime >= timeLimit :
                    timeLimitExceed = True
                    break
                if (tempInternStatus[j] == True) and (nodesDistance[j] < minumumDistance) :
                    minumumDistance = nodesDistance[j]
                    tempInternStatus[j] = False
                    tempNode = j
            tempStatus[tempNode] = False
            tempNodes.append(nodes[tempNode])
            tempNumberNodes.append(tempNode)
            tempInternStatus = tempStatus.copy()
            minumumDistance = sys.float_info.max
            possibleNodes += 1

        kRand = rand.randint(0, possibleNodes)
        status[ tempNumberNodes[kRand] ] = False
        route.append(tempNumberNodes[kRand]+1)
        
        totalDistance += Eu2D(x1, y1, tempNodes[kRand][0], tempNodes[kRand][1])
        x1 = tempNodes[kRand][0]
        y1 = tempNodes[kRand][1]

    route.append(initNumber+1)
    totalDistance += Eu2D( x1, y1, initCoords[0], initCoords[1] )
    realTotalDistance = totalDistance.copy()
    realRoute = route.copy()
    actualTime = time.time() - startTime
    if totalDistance < bestDistance and timeLimitExceed == False:
        bestDistance = realTotalDistance.copy()
        bestRoute = realRoute.copy()
        print( "Cyle: {:,.0f}\t\tBest Distance at the moment: {:,.5f}" .format( a+1, bestDistance ) )

if actualTime >= timeLimit :
    print( "\nTime limit exceeded ({:,.5f} seconds). Terminating program." .format(timeLimit) )

execTime = time.time() - startTime
print( "Route: %s" %bestRoute )
print( "Best distance: {:,.5f} distance units" .format( bestDistance ) )
print( "Executed time: {:,.5f} seconds" .format( execTime ))

tsp.close()