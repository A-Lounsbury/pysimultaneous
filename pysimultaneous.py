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
    rationality = -1
    
    def __init__(self,numStrats = 2, rationality = 0):
        self.numStrats = numStrats
        self.rationality = rationality

class simGame:
    numPlayers = -1
    payoffMatrix = []
    players = []
    
    mixedEquilibria = []
    pureEquilibria = []
    
    impartial = False
    
    def __init__(self, numPlayers = 2):
        numStrats = [2 for i in range(numPlayers)]
        rationalities = [0 for i in range(numPlayers)]
        self.players = [Player(numStrats[i], rationalities[0]) for i in range(numPlayers)]
        
        self.numPlayers = numPlayers
        self.payoffMatrix = []
        self.impartial = False
        if self.numPlayers < 3:
            matrix = []
            for i in range(self.players[0].numStrats):
                row = []
                for j in range(self.players[1].numStrats):
                    outcome = ListNode(0, True)
                    outcome.append(0, True)
                    row.append(outcome)                        
                matrix.append(row)
            self.payoffMatrix.append(matrix)
                
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
                    self.payoffMatrix[0][i][j].printLL()
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
                
    def removeStrategy(self, x, s):
        """Removes strategy s from player x in the payoff matrix

        Args:
            x (int): index of the player
            s (int): index of the strategy
        """
        if x == 0: # x is player 1
            for m in range(len(self.payoffMatrix)):
                del self.payoffMatrix[m][s]
        if x == 1: # x is player 2
            for m in range(len(self.payoffMatrix)):
                del self.payoffMatrix[m][i][s]
        else: # x > 1
            numErased = 0
            product = 1
            m = 0
            end = [0 for i in range(self.numPlayers)]
            for y in range(self.numPlayers):
                if y != x:
                    end[y] = self.players[y].numStrats
                else:
                    end[y] = s
            
            profile = [0 for i in range(self.numPlayers)]
            while m < self.hash(end):
                profile = unhash(m)
                profile[x] = s # at start of section
                num = 1
                if x < self.numPlayers - 1:
                    for y in range(2, self.numPlayers):
                        if y != x:
                            num *= self.players[y].numStrats
                elif x == self.numPlayers - 1 and self.numPlayers > 3:
                    num = self.players[x].numStrats
                else:
                    print("Error: unexpected values for x and numPlayers")
                
                while numErased < num:
                    del self.payoffMatrix[hash(profile)]
                    numErased += 1
                    
                    # last player's matrices are all lined up; others' must be found
                    if x < self.numPlayers - 1:
                        print()
                        if profile[2] > 0: # simply decrement first number
                            profile[2] -= 1
                        else: # go through each succeeding number
                            y = 2
                            foundNonzero = False
                            while True:
                                profile[y] = self.players[y].numStrats - 1
                                # not last number and next number is nonzero
                                if y != self.numPlayers - 1 and profile[y + 1] != 0:
                                    profile[y + 1] -= 1
                                    foundNonzero = True
                                elif y != self.numPlayers - 1 and profile[y + 1] == 0:
                                    profile[y] = self.players[y].numStrats - 1
                                elif y == self.numPlayers - 1:
                                    profile[y] -= 1
                                y += 1
                                
                                if y >= self.numPlayers or profile[y] != 0 or foundNonzero:
                                    break
                                
                        incremented = False
                        y = 2
                        while not incremented and y < self.numPlayers:
                            if y != x:
                                if profile[y] != self.players[y].numStrats - 1:
                                    profile[y] += 1
                                    incremented = True
                            y += 1
                if x > 2 and x < self.numPlayers - 1 and product == 1:
                    for y in range(2, x - 1):
                        product *= self.players[y].numStrats
                m += product # move to the next one, which is the first in the next section
        self.players[x].numStrats -= 1
        
        if self.impartial:
            impartial = False        
    
    def saveToFile(self, fileName):
        """Saves the data of a game to a text file

        Args:
            fileName (str): the file name
        """
        with open(fileName, 'w') as file:
            file.write(str(self.numPlayers) + "\n")
            
            # write numStrats to file
            for x in range(self.numPlayers):
                file.write(str(self.players[x].numStrats))
                if x < self.numPlayers - 1:
                    file.write(" ")
            file.write("\n")
            
            # write rationalities to the file
            for x in range(self.numPlayers):
                file.write(str(self.players[x].rationality))
                if x < self.numPlayers - 1:
                    file.write(" ")
            file.write("\n")
            
            # write payoffMatrix to file
            for m in range(len(self.payoffMatrix)):
                for i in range(self.players[0].numStrats):
                    for j in range(self.players[1].numStrats):
                        curList = self.payoffMatrix[m][i][j]
                        for x in range(self.numPlayers):
                            file.write(str(curList.getListNode(x).payoff))
                            if x < self.numPlayers - 1:
                                file.write(" ")
                        if j < self.players[1].numStrats - 1:
                            file.write(" ")
                    if i < self.players[0].numStrats - 1:
                        file.write("\n")
                if m < len(self.payoffMatrix) - 1:
                    file.write("\n\n")
            print("Saved to " + fileName + ".\n")
    
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

G = simGame(2)
print("G:")
G.printGame()

G.saveToFile("save.txt")

# print("hash:", G.hash([1, 1, 0]))
# print("unhash:", G.unhash(0))

G.removeStrategy(0, 1)

print("G after:")
G.printGame()

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