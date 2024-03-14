# pysimultaneous.py
# Author: Andrew Lounsbury
# Date: 3/12/24
# Description: a class for handling simultaneous games with n players, n >= 2

class ListNode:
    head = None
    payoff = -1
    bestResponse = True
    next = None
    
    def __init__(self, payoff, bestResponse):
        self.head = self
        self.payoff = 0
        self.bestResponse = False
        self.next = None

    def append(self, payoff, bestResponse):
        newNode = ListNode(payoff, bestResponse)
        if self.head is None:
            self.head = newNode
            return
        
        curNode = self.head
        while curNode.next:
            curNode = curNode.next
        
        curNode.next = newNode
        
    def getListNode(self, index):
        if self.head == None:
            return
 
        curNode = self.head
        pos = 0
        if pos == index:
            return curNode
        else:
            while(curNode != None and pos + 1 != index):
                pos = pos + 1
                curNode = curNode.next
 
            if curNode != None:
                return curNode
            else:
                print("Index not present")
                
    def getPayoff(self):
        return self.payoff

    def insertAtBeginning(self, payoff, bestResponse):
        newNode = ListNode(payoff, bestResponse)
        if self.head is None:
            self.head = newNode
            return
        else:
            newNode.next = self.head
            self.head = newNode
            
    def insertAtIndex(self, data, index):
        newNode = ListNode(data)
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
        
    def pop(self):
        if self.head is None:
            return
    
        curNode = self.head
        while(curNode.next.next):
            curNode = curNode.next
    
        curNode.next = None
                
    def printLL(self):
        curNode = self.head
        size = self.sizeOfLL()
        i = 0
        while(curNode):
            if i < size - 1:
                print(curNode.payoff, end=", ")
            else:
                print(curNode.payoff, end=" ")
            curNode = curNode.next
            i += 1
            
    def printListNode(self, end=""):
        print(self.payoff, end=end)
    
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
                
    def decapitate(self):
        """Removes the head ListNode
        """
        if self.head == None:
            return
        
        self.head = self.head.next
    
    def sizeOfLL(self):
        size = 0
        if(self.head):
            current_node = self.head
            while(current_node):
                size = size + 1
                current_node = current_node.next
            return size
        else:
            return 0
        
    def updateListNode(self, val, index):
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
    
    impartial = False
    
    def __init__(self, numPlayers = 2):
        numStrats = [2 for i in range(numPlayers)]
        self.players = [Player(numStrats[i]) for i in range(numPlayers)]
        
        self.numPlayers = numPlayers
        self.payoffMatrix = []
        self.impartial = False
        if self.numPlayers < 3:
            for i in range(self.players[0].numStrats):
                row = []
                for j in range(self.players[1].numStrats):
                    outcome = ListNode(0, True)
                    outcome.append(0, True)
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
                        outcome = ListNode(0, True)
                        for x in self.players:
                            outcome.append(0, True)
                        row.append(outcome)                 
                    matrix.append(row)
                self.payoffMatrix.append(matrix)
        return
    
    def computeImpartiality(self):
        """ ? 
        """
        num = self.players[0].numStrats
        for x in range(1, self.numPlayers):
            if self.players[x].numStrats != num:
                self.impartial = False
                return
        impartial = True
    
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
        
        if self.numPlayers < 3:
            for i in range(self.players[0].numStrats):
                if self.payoffMatrix[p1Strat][p2Strat].getListNode(0).payoff < self.payoffMatrix[i][p2Strat].getListNode(0).payoff:
                    p1BR = False
            
            for j in range(self.players[1].numStrats):
                if self.payoffMatrix[p1Strat][p2Strat].getListNode(1).payoff < self.payoffMatrix[p1Strat][j].getListNode(1).payoff:
                    p2BR = False
            return (p1BR, p2BR)
        else:
            for m in range(len(self.payoffMatrix)):
                for i in range(self.players[0].numStrats):
                    if self.payoffMatrix[p1Strat][p2Strat].getListNode(0).payoff < self.payoffMatrix[i][p2Strat].getListNode(0).payoff:
                        p1BR = False
                
                for j in range(self.players[1].numStrats):
                    if self.payoffMatrix[p1Strat][p2Strat].getListNode(1).payoff < self.payoffMatrix[p1Strat][j].getNode[1].payoff:
                        p2BR = False
                        
    def hash(self, profile):
        """Converts a sequence of strategies into the index in a stack of payoff arrays that correspond to that sequence

        Args:
            profile (list): strategy profile (indices)

        Returns:
            int: the desired index
        """
        self.computeImpartiality() # ? 
        
        # c_2 + sum_{x = 3}^{nP - 1} (nS)^x * c_x
        num = 0 # return 0 if numPlayers < 2
        if self.numPlayers > 2:
            num = profile[2]
        if self.impartial:
            for x in range(3, self.numPlayers):
                if profile.at(x) > 0:
                    num += self.players[0]**(x - 2) * self.profile[x]
        else: # c_2 + sum_{x=3}^{nP} nS_2 *...* nS_{x-1} * c_x
            if self.numPlayers > 3:
                product = 0
                for x in range(3, numPlayers):
                    product = 1
                    if profile[x] > 0:
                        for y in range(2, x - 1):
                            product *= self.players[y].numStrats
                            
                        num += product * profile[x]
        return num
    
    def printGame(self):
        """Prints the payoff matrix
        """
        if self.numPlayers < 3:
            for i in range(self.players[0].numStrats):
                for j in range(self.players[1].numStrats):
                    self.payoffMatrix[i][j].printLL()
                    if j == self.players[1].numStrats - 1:
                        print()
            print()
        else:
            for m in range(len(self.payoffMatrix)):
                for i in range(self.players[0].numStrats):
                    for j in range(self.players[1].numStrats):
                        self.payoffMatrix[m][i][j].printLL()
                        if j == self.players[1].numStrats - 1:
                            print()
                        print()
                print()
                
    def removeStrategy(x, s):
        """Removes strategy s from player x in the payoff matrix

        Args:
            x (int): index of the player
            s (int): index of the strategy
        """
        if x == 0:
            for m in range(len(self.payoffMatrix)):
                return
        if x == 1:
            for m in range(len(self.payoffMatrix)):
                return
        else:
            numErased = 0
            product = 1
            m = 0
     
    def unhash(self, m):
        """Converts an index in a stack of payoff arrays into the sequence of strategies that produce that index

        Args:
            m (int): the index of the payoff array that we're unhashing

        Returns:
            list: a list of indices (strategies)
        """
        choice = 0
        prevValues = 0 # values from players below P_x
        productNumStrats = 1
        profile = [0 for i in range(self.numPlayers)]
        profile[0] = -1
        profile[1] = -1
        
        for x in range(2, self.numPlayers - 1):
            productNumStrats *= self.players[x].numStrats
            
        for x in range(self.numPlayers - 1, 1, -1):
            choice = 0
            while productNumStrats * choice + prevValues < m and choice != self.players[x].numStrats - 1:
                choice += 1
            
            if productNumStrats * choice + prevValues > m:
                choice -= 1
                
            prevValues += productNumStrats * choice
            profile[x] = choice
            productNumStrats = productNumStrats / self.players[x].numStrats
        return profile

G = simGame(3)
print("G:")
G.printGame()

print("hash:", G.hash([1, 1, 0]))

print("unhash:", G.unhash(0))

# newPayoffs = [[[-3, -3], [0, -5]], [[-5, 0], [-1, -1]]]

# G.enterPayoffs(newPayoffs)
# G.printGame()

# strat1 = 0
# strat2 = 0
# result = G.isBestResponse(strat1, strat2)

# if result[0]:
#     print("YES")
# else:
#     print("NO")
    
# if result[1]:
#     print("YES")
# else:
#     print("NO")
    
# print()
# strat1 = 1
# strat2 = 1
# result = G.isBestResponse(strat1, strat2)

# if result[0]:
#     print("YES")
# else:
#     print("NO")
    
# if result[1]:
#     print("YES")
# else:
#     print("NO")