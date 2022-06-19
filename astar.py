import queue
import sys

class Astar:
    def __init__(self,window):
        self.window = window
        self.maze = self.window.maze
        self.steps = []
        self.color = 0

        # algoritm tukaj
        self.mazeWidth = len(self.maze[0])  # Visina matrike
        self.mazeHeight = len(self.maze)  # Sirina matrike
        self.maxDepth = 0
        self.compCount = 0
        treasureNodes = []  # Seznam koordinat zakladov
        startNode = []  # Koordinate zacetnega polja
        endNode = []  # Koordinate koncnega polja

        cost = 0  # Cena

        # Poisci koordinate vseh zakladov, ter zacetnega in koncnega polja
        for i in range(self.mazeHeight):
            if (-2 in self.maze[i]):
                startNode = [i, self.maze[i].index(-2)]
            if (-4 in self.maze[i]):
                endNode = [i, self.maze[i].index(-4)]
            if (-3 in self.maze[i]):
                for j in range(self.mazeWidth):
                    if (self.maze[i][j] == -3):
                        treasureNodes.append([i, j])

        color = 0
        tempStartNode = startNode
        while (True):
            tempcost, ind = self.search(tempStartNode, endNode, treasureNodes, color)
            tempStartNode = treasureNodes[ind][:]
            del treasureNodes[ind]
            cost += tempcost
            color += 1
            if (not treasureNodes):
                tempcost, ind = self.search(tempStartNode, endNode, treasureNodes, color)
                break
        cost += tempcost
        self.window.setSteps(self.steps,cost,self.maxDepth,self.compCount)

        print("Pot")
        print(str(list(i[:2] for i in self.steps))[1:-1].replace("[", "(").replace("]", ")"))
        print("Cena")
        print(cost)
        print("Premiki")
        print(len(self.steps))
        print("Maksimalna globina")
        print(self.maxDepth)
        print("Primerjave")
        print(self.compCount)

    def search(self, startNode, endNode, treasureNodes, color):
        moveNode = [[0, 1], [-1, 0], [0, -1], [1, 0]]  # Seznam moznih premikov
        closedNodes = [[]] * self.mazeHeight  # Matrika vseh obiskanih polj
        fromNode = [[]] * self.mazeHeight  # Matrika prejsnjih polj
        for i in range(self.mazeHeight):
            closedNodes[i] = [False] * self.mazeWidth
            fromNode[i] = [None] * self.mazeWidth
        fromNode[startNode[0]][startNode[1]] = -1
        open = queue.PriorityQueue()
        closedNodes[startNode[0]][startNode[1]] = True
        open.put([0, startNode])
        nodeCost = 0
        steps = []
        while (open):
            if (open.qsize() > self.maxDepth):
                self.maxDepth = open.qsize()
            currentNode = open.get()[1]
            print("Odstranjujem iz vrste vozlisce ", currentNode)

            if (currentNode not in closedNodes):
                closedNodes[currentNode[0]][currentNode[1]] = True
            if ((treasureNodes and currentNode in treasureNodes) or (not treasureNodes and currentNode == endNode)):
                print("Resitev BFS v vozliscu ", currentNode)
                print("Pot:", currentNode)
                steps.append([*currentNode,color,"path"])
                ind = None
                if (currentNode in treasureNodes):
                    ind = treasureNodes.index(currentNode)
                while (True):
                    currentNode = fromNode[currentNode[0]][currentNode[1]]
                    if (currentNode != startNode):
                        if (self.maze[currentNode[0]][currentNode[1]] > 0):
                            nodeCost += self.maze[currentNode[0]][currentNode[1]]
                        print(" <-- ", currentNode)
                        steps.append([*currentNode, color, "path"])
                    else:
                        break
                self.steps += reversed(steps)
                return nodeCost, ind
            for i in range(4):
                self.compCount += 1
                nextNode = moveNode[i][:]
                nextNode[0] += currentNode[0]
                nextNode[1] += currentNode[1]
                if (nextNode[0] == self.mazeHeight):
                    nextNode[0] -= 1
                if (nextNode[1] == self.mazeWidth):
                    nextNode[1] -= 1
                if (nextNode[0] >= 0 and nextNode[0] < self.mazeHeight and nextNode[1] >= 0 and nextNode[
                    1] < self.mazeWidth):
                    if (self.maze[nextNode[0]][nextNode[1]] != -1 and not closedNodes[nextNode[0]][nextNode[1]]):
                        closedNodes[nextNode[0]][nextNode[1]] = True
                        open.put([abs(nextNode[0]-endNode[0]) + abs(nextNode[1] - endNode[1]) + self.maze[nextNode[0]][nextNode[1]], nextNode])
                        fromNode[nextNode[0]][nextNode[1]] = currentNode
        # self.window.changeCell(10,10,True)
        # self.window.changeCell(10,10,False)
