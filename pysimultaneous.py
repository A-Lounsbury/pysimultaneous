# pysimultaneous.py
# Author: Andrew Lounsbury
# Date: 3/12/24
# Description: a class for handling simultaneous games with n players, n >= 2

class Node:
    def __init__(self, payoff, bestResponse):
        self.payoff = 0
        self.bestResponse = False
        self.next = None

    def insertAtBeginning(self, payoff, bestResponse):
        newNode = Node(payoff, bestResponse)
        if self.head is None:
            self.head = newNode
            return
        else:
            newNode.next = self.head
            self.head = newNode
            
    def insertAtIndex(self, data, index):
        newNode = Node(data)
        curNode = self.head
        pos = 0
        if pos == index:
            self.insertAtBegin(data)
        else:
            while curNode != None and pos + 1 != index:
                pos = pos + 1
                curNode = curNode.next
 
            if curNode != None:
                newNode.next = curNode.next
                curNode.next = newNode
            else:
                print("Index not present")
    
    def append(self, payoff, bestResponse):
        newNode = Node(payoff, bestResponse)
        if self.head is None:
            self.head = newNode
            return
        
        curNode = self.head
        while(curNode.next):
            curNode = curNode.next
        
        curNode.next = newNode
        
    def updateNode(self, val, index):
        curNode = self.head
        pos = 0
        if pos == index:
            curNode.data = val
        else:
            while curNode != None and pos != index:
                pos = pos + 1
                curNode = curNode.next
    
            if curNode != None:
                curNode.data = val
            else:
                print("Index not present")
            
    def removeFirstNode(self):
        if self.head == None:
            return
        
        self.head = self.head.next
        
    def pop(self):
        if self.head is None:
            return
    
        curNode = self.head
        while(curNode.next.next):
            curNode = curNode.next
    
        curNode.next = None
        
    def removeAtIndex(self, index):
        if self.head == None:
            return
 
        curNode = self.head
        pos = 0
        if pos == index:
            self.remove_first_node()
        else:
            while(curNode != None and pos + 1 != index):
                pos = pos + 1
                curNode = curNode.next
 
            if curNode != None:
                curNode.next = curNode.next.next
            else:
                print("Index not present")
                
    def printLL(self):
        curNode = self.head
        while(curNode):
            print(curNode.data)
            curNode = curNode.next
    
    def sizeOfLL(self):
        size = 0
        if(self.head):
            current_node = self.head
            while(current_node):
                size = size+1
                current_node = current_node.next
            return size
        else:
            return 0

class Player:
    numStrats = -1
    
    def __init__(self,numStrats = 2):
        self.numStrats = numStrats

class simGame:
    numPlayers = -1
    payoffMatrix = []
    players = []
    
    mixedEquilibria = []
    pureEquilibria = []
    
    def __init__(self, numPlayers = 2):
        numStrats = [2 for i in range(numPlayers)]
        self.players = [Player(numStrats[i]) for i in range(numPlayers)]
        
        self.numPlayers = numPlayers
        self.payoffMatrix = []
        if self.numPlayers < 3:
            for i in range(self.players[0].numStrats):
                row = []
                for j in range(self.players[1].numStrats):
                    outcome = []
                    for x in self.players:
                        outcome.append(0)
                    row.append(outcome)                        
                self.payoffMatrix.append(row)
        else:
            numMatrices = 1
            for i in range(3, self.numPlayers):
                numMatrices *= self.players[i].numStrats
            for m in range(numMatrices):
                matrix = []
                for i in range(self.players[0].numStrats):
                    row = []
                    for j in range(self.players[1].numStrats):
                        outcome = []
                        for x in self.players:
                            outcome.append(0)
                        row.append(outcome)                 
                    matrix.append(row)
                self.payoffMatrix.append(matrix)
                
        return
    
    def enterPayoffs(self, payoffs = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]):
        self.payoffMatrix = payoffs
        
    def isBestResponse(self, p1Strat, p2Strat):
        """Checks whether p1Strat and p2Strat are best responses relative to each other

        Args:
            p1Strat (int): p1's strategy
            p2Strat (int): p2's strategy
        """
        p1BR = True
        p2BR = True
        
        for i in range(self.players[0].numStrats):
            if self.payoffMatrix[p1Strat][p2Strat][0] < self.payoffMatrix[i][p2Strat][0]:
                p1BR = False
        
        for j in range(self.players[1].numStrats):
            if self.payoffMatrix[p1Strat][p2Strat][1] < self.payoffMatrix[p1Strat][j][1]:
                p2BR = False
        return (p1BR, p2BR)
        
    
    def printGame(self):
        """Prints the payoff matrix
        """
        if self.numPlayers < 3:
            for i in range(self.players[0].numStrats):
                for j in range(self.players[1].numStrats):
                    for n in range(self.numPlayers):
                        if n < self.numPlayers - 1:
                            print(self.payoffMatrix[i][j][n], end=", ")
                        else:
                            print(self.payoffMatrix[i][j][n], end="")
                    print(" ", end="")
                print()
        else:
            for m in range(len(self.payoffMatrix)):
                for i in range(self.players[0].numStrats):
                    for j in range(self.players[1].numStrats):
                        for n in range(self.numPlayers):
                            if n < self.numPlayers - 1:
                                print(self.payoffMatrix[m][i][j][n], end=", ")
                            else:
                                print(self.payoffMatrix[m][i][j][n], end="")
                        print(" ", end="")
                    print()
                print()
            
G = simGame(3)
G.printGame()

# newPayoffs = [[[-3, -3], [0, -5]], [[-5, 0], [-1, -1]]]

# G.enterPayoffs(newPayoffs)
G.printGame()

strat1 = 0
strat2 = 0
result = G.isBestResponse(strat1, strat2)

if result[0]:
    print("YES")
else:
    print("NO")
    
if result[1]:
    print("YES")
else:
    print("NO")
    
print()
strat1 = 1
strat2 = 1
result = G.isBestResponse(strat1, strat2)

if result[0]:
    print("YES")
else:
    print("NO")
    
if result[1]:
    print("YES")
else:
    print("NO")