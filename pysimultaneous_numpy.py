# pysimultaneous_numpy.py
# Author: Andrew Lounsbury
# Date: 3/16/24
# Description: a class for handling simultaneous games with n players, n >= 2. Payoffs for each player are stored in their own individual numpy array. 
import numpy as np

class Player:
    numStrats = -1
    rationality = -1
    
    def __init__(self,numStrats = 2, rationality = 0):
        self.numStrats = numStrats
        self.rationality = rationality

class simGame:    
    kMatrix = []
    impartial = False
    kOutcomes = [] # n-tuples that appear in kMatrix; won't be all of them
    kStrategies = [[] for i in range(4)] # 2D matrix containing the strategies each player would play for k-levels 0, 1, 2, 3
    mixedEquilibria = []
    numPlayers = -1
    payoffMatrix = [] # numPlayers long, contains the players' individual payoff matrices
    players = []
    pureEquilibria = []
    rationalityProbabilities = [0.0 for i in range(4)] # probability a player is L_i, i = 0, 1, 2, 3
    strategyNames = []
    
    def __init__(self, numPlayers = 2):
        numStrats = [2 for i in range(numPlayers)]
        rationalities = [0 for i in range(numPlayers)]
        self.players = [Player(numStrats[i], rationalities[0]) for i in range(numPlayers)]
        
        # Creating kStrategies' 4 arrays of lists of size numPlayers and setting rationalityProbabilities
        for r in range(4):
            # resizing self.kStrategies[r]
            if numPlayers > len(self.kStrategies[r]):
                self.kStrategies[r] += [None] * (numPlayers - len(self.kStrategies[r]))
            else:
                self.kStrategies[r] = self.kStrategies[r][:numPlayers]
            self.rationalityProbabilities[r] = 0.0
        
        # Initializing strategy names
        if self.players[0].numStrats < 3:
            self.strategyNames.append(["U", "D"])
        else:
            self.strategyNames.append(["U"] + ["M" + str(i) for i in range(1, self.players[0].numStrats)] + ["D"])
        if self.players[1].numStrats < 3:
            self.strategyNames.append(["L", "R"])
        else:
            self.strategyNames.append(["L"] + ["C" + str(i) for i in range(self.players[0].numStrats)] + ["R"])
        for x in range(2, self.numPlayers):
            if self.players[x].numStrats < 3:
                self.strategyNames.append(["L(" + str(x) + ")", "R(" + str(x) + ")"])
            else: 
                self.strategyNames.append(["L(" + str(x) + ")"] + ["C(" + str(x) + ", " + str(i) + ")" for i in range(self.players[0].numStrats)] + ["R(" + str(x) + ")"])
        
        self.numPlayers = numPlayers
        self.payoffMatrix = []
        self.impartial = False
        
        # Creating payoff matrix
        if self.numPlayers < 3:
            dimensions = tuple([self.players[x].numStrats for x in range(self.numPlayers)])
        else:
            product = 1
            for x in range(2, self.numPlayers):
                product *= self.players[x].numStrats
            dimensions = tuple([product] + [self.players[x].numStrats for x in range(2)])
            
        for x in range(self.numPlayers):
            self.payoffMatrix.append(np.zeros(dimensions))
        return
    
    def computeImpartiality(self):
        """ Checks if players 2,...,numPlayers have the same number of strategies as player 1? 
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
                if self.payoffMatrix[0][p1Strat][p2Strat] < self.payoffMatrix[0][i][p2Strat]:
                    p1BR = False
            for j in range(self.players[1].numStrats):
                if self.payoffMatrix[1][p1Strat][p2Strat] < self.payoffMatrix[1][p1Strat][j]:
                    p2BR = False
            return (p1BR, p2BR)
        else: # FIXME
            for m in range(self.payoffMatrix[0].size):
                for i in range(self.players[0].numStrats):
                    if self.payoffMatrix[0][m][p1Strat][p2Strat] < self.payoffMatrix[0][m][i][p2Strat]:
                        p1BR = False
                for j in range(self.players[1].numStrats):
                    if self.payoffMatrix[1][m][p1Strat][p2Strat] < self.payoffMatrix[1][m][p1Strat][j]:
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
                    num += self.players[0] ** (x - 2) * self.profile[x]
        else: # c_2 + sum_{x=3}^{nP} nS_2 *...* nS_{x-1} * c_x
            if self.numPlayers > 3:
                product = 0
                for x in range(3, self.numPlayers):
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
            print(self.payoffMatrix[0])
        else:
            for x in range(self.numPlayers):
                print(self.payoffMatrix[x])
                print()

    def readFromFile(self, fileName):
        addMoreOutcomesPast2 = False # kMatrix
        nP = -1 # numPlayers
        nS = -1 # numStrats
        r = -1 # rationality
        oldNumPlayers = -1
        oldNumStrats = [-1 for i in range(self.numPlayers)]
        oldSize = -1
        curList = []
        
        with open(fileName, 'r') as file:
            oldNumPlayers = self.numPlayers
            
            for x in range(self.numPlayers):
                oldNumStrats[x] = self.players[x].numStrats
                
            oldSize = len(self.payoffMatrix)
            
            # reading numPlayers
            nP = file.readline()
            self.numPlayers = int(nP)
            
            # reading numStrats for old players
            if oldNumPlayers <= self.numPlayers:
                nS = file.readline().split(" ")
                for n in nS:
                    n = n.rstrip()
                # Getting rationalities
                rats = file.readline().split(" ")
                for rat in rats:
                    rat = rat.rstrip()
                               
                for x in range(oldNumPlayers):
                    self.players[x].numStrats = int(nS[x])
                    self.players[x].rationality = int(rats[x])
            else:
                nS = file.readline().split(" ")
                for n in nS:
                    n = int(n.rstrip())
                # Getting rationalities
                rats = file.readline.split(" ")
                for rat in rats:
                    rat = int(rat.rstrip())
                
                for x in range(numPlayers):
                    self.players[x].numStrats = int(nS[x])
                    self.players[x].rationality = rats[x]
            
            """
			add new players if there are more,
			resizing payoffMatrix and kMatrix,
			increase the size of kStrategy lists 
            """
            if oldNumPlayers != self.numPlayers:
                if oldNumPLayers < numPlayers:
                    addMoreOutcomesPast2 = True
                # Create new players and read rest of numStrats
                for x in range(oldNumPlayers, self.numPlayers):
                    p = Player(int(nS[x]), rats[x])
                    players.append(p)
                    
            # FIXME
            # new matrices added to the end
            size = 1
            if self.numPlayers > 2:
                for x in range(2, self.numPlayers):
                    size *= self.players[x].numStrats
            if size > len(self.payoffMatrix):
                self.payoffMatrix += [None] * (size - len(self.payoffMatrix))
            else:
                self.payoffMatrix = self.payoffMatrix[:size]
            
            size = 1
            if self.numPlayers > 2:
                size = 4 ** (self.numPlayers - 2)
            if size > len(self.kMatrix):
                self.kMatrix += [None] * (size - len(self.kMatrix))
            else:
                self.kMatrix = self.kMatrix[:size]
            
            # FIXME
            # creating/deleting entries and reading values
            for m in range(len(self.payoffMatrix)):
                if self.players[0].numStrats > len(self.payoffMatrix[m]):
                    self.payoffMatrix[m] += [None] * (self.players[0].numStrats - len(self.payoffMatrix[m]))
                else:
                    self.payoffMatrix[m] = self.payoffMatrix[m][:self.players[0].numStrats]
                for i in range(self.players[0].numStrats):
                    # resizing
                    if self.players[1].numStrats > len(self.payoffMatrix[m][i]):
                        self.payoffMatrix[m][i] += [None] * (self.players[1].numStrats - len(self.payoffMatrix[m][i]))
                    else:
                        self.payoffMatrix[m][i] = self.payoffMatrix[m][i][:self.players[1].numStrats]
                    # Reading in the next row of payoffs
                    payoffs = file.readline().split(" ")
                    for payoff in payoffs:
                        payoff = int(payoff.rstrip())
                    groupedPayoffs = [payoffs[i:i + self.numPlayers] for i in range(0, len(payoffs), self.numPlayers)]
                    
                    for j in range(self.players[1].numStrats):
                        # Create new list if needed
                        if not self.payoffMatrix[m][i][j]:
                            newList = ListNode(0, False)
                            self.payoffMatrix[m][i][j] = newList
                        curList = self.payoffMatrix[m][i][j]
                        while curList.sizeOfLL() > self.numPlayers:
                            # Deleting
                            curList.removeAtIndex(curList.sizeOfLL() - 1)
                        
                        for x in range(self.numPlayers):
                            if m < oldSize and x < oldNumPlayers and i < oldNumStrats[0] and j < oldNumStrats[1]: # old matrix, old outcome, old payoff
                                curList.updateListNode(int(groupedPayoffs[j][x]), x) # inserting payoff value
                            else: # Everything is new
                                # Adding
                                curList.appendNode(int(payoffs[x]), False)
            
            if addMoreOutcomesPast2:
                for m in range((len(self.kMatrix))):
                    if 4 > len(self.kMatrix[m]):
                        self.kMatrix[m] += [None] * (4 - len(self.kMatrix[m]))
                    else:
                        self.kMatrix[m] = self.kMatrix[m][:4]
                    for i in range(4):
                        if 4 > len(self.kMatrix[m]):
                            self.kMatrix[m][i] += [None] * (4 - len(self.kMatrix[m][i]))
                        else:
                            self.kMatrix[m][i] = self.kMatrix[m][i][:4]
                        for j in range(4):
                            myList = [-1 for l in range(self.numPlayers)]
                            kMatrix[m][i][j] = myList
        print("Done reading from " + fileName)

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
            
            # FIXME
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

G = simGame(3)
print("G:")
G.printGame()

print(G.payoffMatrix[0][0][0][0])

results = G.isBestResponse(0, 0)
print(results)