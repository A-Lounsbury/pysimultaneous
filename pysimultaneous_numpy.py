# pysimultaneous_numpy.py
# Author: Andrew Lounsbury
# Date: 3/17/24
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
        # Creating players
        numStrats = [2 for x in range(numPlayers)]
        rationalities = [0 for x in range(numPlayers)]
        self.players = [Player(numStrats[x], rationalities[0]) for x in range(numPlayers)]
        
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
        
        # Creating dimensions for payoff matrix
        if self.numPlayers < 3:
            dimensions = tuple([self.players[x].numStrats for x in range(self.numPlayers)])
        else:
            product = 1
            for x in range(2, self.numPlayers):
                product *= self.players[x].numStrats
            dimensions = tuple([product] + [self.players[x].numStrats for x in range(2)])
            
        # Appending one matrix of payoffs for each player
        for x in range(self.numPlayers):
            self.payoffMatrix.append(np.zeros(dimensions))
        return
    
    def enterPayoffs(self, payoffs, numPlayers = 2, numStrats = [2, 2]):
        """Enters the payoffs into the payoff matrix and updates self.numPlayers and each player's numStrats. 

        Args:
            payoffs (numpy array): the payoffs to be entered. 
            numPlayers (int): the number of players. Defaults to 2. 
            numStrats (list): a list of integers that are the new numbers of strategies for each player. Defaults to [2, 2]. 
        """
        if numPlayers != len(numStrats):
            print("Error (enterPayoffs): the number of numStrats did not match the given number of players.")
            return
        self.numPlayers = numPlayers
        for x in range(self.numPlayers):
            self.players[x].numStrats = numStrats[x]
        self.payoffMatrix = []
        for ar in payoffs:
            self.payoffMatrix.append(ar)
    
    def isBestResponse(self, profile):
        """Checks whether p1Strat and p2Strat are best responses relative to each other

        Args:
            p1Strat (int): p1's strategy
            p2Strat (int): p2's strategy
        """
        br = [True for x in range(self.numPlayers)]
        
        if self.numPlayers < 3:
            for i in range(self.players[0].numStrats):
                if self.payoffMatrix[0][profile[0]][profile[1]] < self.payoffMatrix[0][i][profile[1]]:
                    br[0] = False
            for j in range(self.players[1].numStrats):
                if self.payoffMatrix[1][profile[0]][profile[1]] < self.payoffMatrix[1][profile[0]][j]:
                    br[1] = False
        else:
            for x in range(self.numPlayers):
                if x < 2:
                    for i in range(self.players[0].numStrats):
                        if self.payoffMatrix[0][self.toIndex(profile)][profile[0]][profile[1]] < self.payoffMatrix[0][self.toIndex(profile)][i][profile[1]]:
                            br[0] = False
                    for j in range(self.players[1].numStrats):
                        if self.payoffMatrix[1][self.toIndex(profile)][profile[0]][profile[1]] < self.payoffMatrix[1][self.toIndex(profile)][profile[0]][j]:
                            br[1] = False
                else:
                    for m in range(self.payoffMatrix[0].shape[0]):
                        compProfile = profile # "compare profile"
                        compProfile[x] = m
                        if self.payoffMatrix[x][self.toIndex(profile)][profile[0]][profile[1]] < self.payoffMatrix[x][self.toIndex(compProfile)][profile[1]][profile[2]]:
                            br[x] = False
        return br
    
    def print(self):
        """Prints the payoff matrix
        """
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
            if file.readline().strip() == "together": 
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
                if size > self.payoffMatrix[0].shape[0]:
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
                    # resizing p1
                    if self.players[0].numStrats > len(self.payoffMatrix[m]):
                        self.payoffMatrix[m] += [None] * (self.players[0].numStrats - len(self.payoffMatrix[m]))
                    else:
                        self.payoffMatrix[m] = self.payoffMatrix[m][:self.players[0].numStrats]
                    for i in range(self.players[0].numStrats):
                        # resizing p2
                        if self.players[1].numStrats > len(self.payoffMatrix[m][i]):
                            self.payoffMatrix[m][i] += [None] * (self.players[1].numStrats - len(self.payoffMatrix[m][i]))
                        else:
                            self.payoffMatrix[m][i] = self.payoffMatrix[m][i][:self.players[1].numStrats]
                        # Reading in the next row of payoffs
                        payoffs = file.readline().split(" ")
                        for payoff in payoffs:
                            payoff = float(payoff.rstrip())
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
            else: # separate
                return
        print("Done reading from " + fileName)

    def removeStrategy(self, player, s):
        """Removes strategy s from player in the payoff matrix

        Args:
            player (int): index of the player
            s (int): index of the strategy
        """
        if player == 0: # player is player 1
            for x in range(self.numPlayers):
                # deleting s-th row from every x-th matrix
                self.payoffMatrix[x] = np.delete(self.payoffMatrix[x], s, axis=0)
        elif player == 1: # player is player 2
            for x in range(self.numPlayers):
                # deleting s-th column from every x-th matrix
                self.payoffMatrix[x] = np.delete(self.payoffMatrix[x], s, axis=1)
        else: # player > 1
            m = 0
            numErased = 0
            product = 1
            numPlayersAbove = self.numPlayers - player - 1
            numPlayersBelow = player - 2
            curProfile = [-1, -1] + [0 for x in range(2, self.numPlayers)]
            numStratsSum = 0
            numStratsSum = sum(self.players[x].numStrats for x in range(player, self.numPlayers))
            start = numPlayersBelow * numStratsSum
            print("start:", start)
            # FIXME
            """For each player x, cycle through the sequence of profiles whose hashes correspond to 
            4, 5, 6, 13, 14, 15, 22, 23, 24, and delete those matrices. 
            OR, select the first matrix and delete it for each player, then select the second 
            matrix and delete it for each player, so on and so forth. 
            """
            print("curProfile", curProfile)
            for x in range(self.numPlayers):
                # starting at the first profile in the sequence
                
                
                # continue until...we've deleted the number of matrices we were supposed to delete? Until the profile or the hash of the profile looks a certain way? 
                k = 0
                while k < 10:                
                    # deleting the matrix
                    # self.payoffMatrix[x] = np.delete(self.payoffMatrix[x], self.toIndex(curProfile), axis=2)
                    k += 1
                
                # obtaining the next profile in the sequence
                
        # Decrement the number of strategies for player
        self.players[player].numStrats -= 1

        return
    
    def saveToFile(self, fileName, together=True):
        """Saves the data of a game to a text file

        Args:
            fileName (str): the file name
        """
        with open(fileName, 'w') as file:
            if together:
                file.write("together\n")
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
                if self.numPlayers < 3:
                    for i in range(self.players[0].numStrats):
                        for j in range(self.players[1].numStrats):
                            for x in range(self.numPlayers):
                                file.write(str(self.payoffMatrix[x][i][j]))
                                if x < self.numPlayers - 1:
                                    file.write(" ")
                            if j < self.players[1].numStrats - 1:
                                file.write(" ")
                        if i < self.players[0].numStrats - 1:
                            file.write("\n")
                else: 
                    for m in range(self.payoffMatrix[0].shape[0]):
                        for i in range(self.players[0].numStrats):
                            for j in range(self.players[1].numStrats):
                                for x in range(self.numPlayers):
                                    file.write(str(self.payoffMatrix[x][m][i][j]))
                                    if x < self.numPlayers - 1:
                                        file.write(" ")
                                if j < self.players[1].numStrats - 1:
                                    file.write(" ")
                            if i < self.players[0].numStrats - 1:
                                file.write("\n")
                        if m < self.payoffMatrix[0].shape[0] - 1:
                            file.write("\n\n")
            else: # separate
                file.write("separate\n")
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
                if self.numPlayers < 3:
                    for i in range(self.players[0].numStrats):
                        for j in range(self.players[1].numStrats):
                            for x in range(self.numPlayers):
                                file.write(str(self.payoffMatrix[x][i][j]))
                                if x < self.numPlayers - 1:
                                    file.write(" ")
                            if j < self.players[1].numStrats - 1:
                                file.write(" ")
                        if i < self.players[0].numStrats - 1:
                            file.write("\n")
                else: 
                    for x in range(self.numPlayers):
                        for m in range(self.payoffMatrix[0].shape[0]):
                            for i in range(self.players[0].numStrats):
                                for j in range(self.players[1].numStrats):
                                    file.write(str(self.payoffMatrix[x][m][i][j]))
                                    if j < self.players[1].numStrats - 1:
                                        file.write(" ")
                                if i < self.players[0].numStrats - 1:
                                    file.write("\n")
                            if m < self.payoffMatrix[0].shape[0] - 1:
                                file.write("\n\n")
                        if x < self.numPlayers - 1:
                            file.write("\n\n")
                return
            print("Saved to " + fileName + ".\n")
    
    def toIndex(self, profile):
        """Converts a sequence of strategies into the index in a stack of payoff arrays that correspond to that sequence. This is the inverse of the function toProfile. 

        Args:
            profile (list): strategy profile (indices)

        Returns:
            int: the desired index
        """
        sameNumStratsPastPlayer2 = True
        # Checking if players 2,...,numPlayers have the same number of strategies as player 3
        for x in range(2, self.numPlayers):
            if self.players[x].numStrats != self.players[1].numStrats:
                self.sameNumStratsPastPlayer2 = False
        
        # c_2 + sum_{x = 3}^{nP - 1} (nS)^x * c_x
        num = 0 # return 0 if self.numPlayers < 3
        if self.numPlayers > 2:
            num = profile[2]
        if sameNumStratsPastPlayer2: # if all players past player 2 have the same number of strategies
            for x in range(3, self.numPlayers):
                if profile[x] > 0:
                    num += (self.players[2].numStrats ** (x - 2)) * profile[x]
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
    
    def toProfile(self, m):
        """Converts an index in a stack of payoff arrays into the sequence of strategies that produce that index. This is the inverse of the function toIndex. 

        Args:
            m (int): the index of the payoff array that we're toProfileing

        Returns:
            list: a list of indices (strategies)
        """
        choice = 0
        prevValues = 0 # values from players below P_x
        productNumStrats = 1
        profile = [0 for x in range(self.numPlayers)]
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

arr_3players = np.array([
    [ # player 1's matrices
        [[1, 1], [1, 1]],
        [[1.1, 1.1], [1.1, 1.1]]
    ],
    [ # player 2's matrices
        [[2, 2], [2, 2]],
        [[2.1, 2.1], [2.1, 2.1]]
    ],
    [ # player 3's matrices
        [[3, 3], [3, 3]],
        [[3.1, 3.1], [3.1, 3.1]]
    ]
])

arr_5players = np.array([
    [ # player 1's matrices
        [[0, 1], [1, 1]], 
        [[1, 1], [1, 1]], 
        [[2, 1], [1, 1]], 
        [[3, 1], [1, 1]], 
        [[4, 1], [1, 1]], 
        [[5, 1], [1, 1]], 
        [[6, 1], [1, 1]], 
        [[7, 1], [1, 1]], 
        [[8, 1], [1, 1]], 
        
        [[9, 1], [1, 1]], 
        [[10, 1], [1, 1]], 
        [[11, 1], [1, 1]], 
        [[12, 1], [1, 1]], 
        [[13, 1], [1, 1]], 
        [[14, 1], [1, 1]], 
        [[15, 1], [1, 1]], 
        [[16, 1], [1, 1]], 
        [[17, 1], [1, 1]], 
        
        [[18, 1], [1, 1]], 
        [[19, 1], [1, 1]], 
        [[20, 1], [1, 1]], 
        [[21, 1], [1, 1]], 
        [[22, 1], [1, 1]], 
        [[23, 1], [1, 1]], 
        [[24, 1], [1, 1]], 
        [[25, 1], [1, 1]], 
        [[26, 1], [1, 1]]
        
    ],
    [ # player 2's matrices
        [[27, 1], [1, 1]],
        [[28, 2], [2, 2]], 
        [[29, 2], [2, 2]], 
        [[30, 2], [2, 2]], 
        [[31, 2], [2, 2]], 
        [[32, 2], [2, 2]], 
        [[33, 2], [2, 2]], 
        [[34, 2], [2, 2]], 
        [[35, 2], [2, 2]], 
        
        [[36, 2], [2, 2]], 
        [[37, 2], [2, 2]], 
        [[38, 2], [2, 2]], 
        [[39, 2], [2, 2]], 
        [[40, 2], [2, 2]], 
        [[41, 2], [2, 2]], 
        [[42, 2], [2, 2]], 
        [[43, 2], [2, 2]], 
        [[44, 2], [2, 2]], 
        
        [[45, 2], [2, 2]],
        [[46, 2], [2, 2]], 
        [[47, 2], [2, 2]], 
        [[48, 2], [2, 2]], 
        [[49, 2], [2, 2]], 
        [[50, 2], [2, 2]], 
        [[51, 2], [2, 2]], 
        [[52, 2], [2, 2]], 
        [[53, 2], [2, 2]]
        
    ],
    [ # player 3's matrices
        [[54, 2], [2, 2]],
        [[55, 3], [3, 3]], 
        [[56, 3], [3, 3]], 
        [[57, 3], [3, 3]], 
        [[58, 3], [3, 3]], 
        [[59, 3], [3, 3]], 
        [[60, 3], [3, 3]], 
        [[61, 3], [3, 3]], 
        [[62, 3], [3, 3]], 
        
        [[63, 3], [3, 3]], 
        [[64, 3], [3, 3]], 
        [[65, 3], [3, 3]], 
        [[66, 3], [3, 3]], 
        [[67, 3], [3, 3]], 
        [[68, 3], [3, 3]], 
        [[69, 3], [3, 3]], 
        [[70, 3], [3, 3]], 
        [[71, 3], [3, 3]], 
        
        [[72, 3], [3, 3]], 
        [[73, 3], [3, 3]], 
        [[74, 3], [3, 3]], 
        [[75, 3], [3, 3]], 
        [[76, 3], [3, 3]], 
        [[77, 3], [3, 3]], 
        [[78, 3], [3, 3]], 
        [[79, 3], [3, 3]], 
        [[80, 3], [3, 3]]
        
    ],
    [ # player 4's matrices
        [[81, 3], [3, 3]],
        [[82, 4], [4, 4]], 
        [[83, 4], [4, 4]], 
        [[84, 4], [4, 4]], 
        [[85, 4], [4, 4]], 
        [[86, 4], [4, 4]], 
        [[87, 4], [4, 4]], 
        [[88, 4], [4, 4]], 
        [[89, 4], [4, 4]], 
        
        [[90, 4], [4, 4]],
        [[91, 4], [4, 4]], 
        [[92, 4], [4, 4]], 
        [[93, 4], [4, 4]], 
        [[94, 4], [4, 4]], 
        [[95, 4], [4, 4]], 
        [[96, 4], [4, 4]], 
        [[97, 4], [4, 4]], 
        [[98, 4], [4, 4]], 
        
        [[99, 4], [4, 4]], 
        [[100, 4], [4, 4]], 
        [[101, 4], [4, 4]], 
        [[102, 4], [4, 4]], 
        [[103, 4], [4, 4]], 
        [[104, 4], [4, 4]], 
        [[105, 4], [4, 4]], 
        [[106, 4], [4, 4]], 
        [[107, 4], [4, 4]]
        
    ],
    [ # player 5's matrices
        [[108, 4], [4, 4]],
        [[109, 5], [5, 5]], 
        [[110, 5], [5, 5]], 
        [[111, 5], [5, 5]], 
        [[112, 5], [5, 5]], 
        [[113, 5], [5, 5]], 
        [[114, 5], [5, 5]], 
        [[115, 5], [5, 5]], 
        [[116, 5], [5, 5]],
         
        [[117, 5], [5, 5]], 
        [[118, 5], [5, 5]], 
        [[119, 5], [5, 5]], 
        [[120, 5], [5, 5]], 
        [[121, 5], [5, 5]], 
        [[122, 5], [5, 5]], 
        [[123, 5], [5, 5]], 
        [[124, 5], [5, 5]], 
        [[125, 5], [5, 5]], 
        
        [[126, 5], [5, 5]], 
        [[127, 5], [5, 5]], 
        [[128, 5], [5, 5]], 
        [[129, 5], [5, 5]], 
        [[130, 5], [5, 5]], 
        [[131, 5], [5, 5]], 
        [[132, 5], [5, 5]], 
        [[133, 5], [5, 5]], 
        [[134, 5], [5, 5]]
        
    ],
])

G = simGame(3)
# G.print()
# print("G:")
G.enterPayoffs(arr_3players, 3, [2, 2, 2])
# G.print()
# G.removeStrategy(2, 0)
# print("G again:")
# G.print()

H = simGame(5)
H.enterPayoffs(arr_5players, 5, [2, 2, 3, 3, 3])
# H.removeStrategy(3, 1)
# H.print()

print("0:", H.toProfile(0))
print("1:", H.toProfile(1))
print("2:", H.toProfile(2))
print("3:", H.toProfile(3))
print()

print("4:", H.toProfile(4))
print("5:", H.toProfile(5))
print("6:", H.toProfile(6))
print("13:", H.toProfile(13))
print("14:", H.toProfile(14))
print("15:", H.toProfile(15))
print("22:", H.toProfile(22))
print("23:", H.toProfile(23))
print("24:", H.toProfile(24))

print("\nG tests:")
print(G.toIndex([-1, -1, 0]))
print(G.toIndex([-1, -1, 1]))
print()

print(G.toProfile(0))
print(G.toProfile(1))
print()

print("[., ., 0]:", G.toProfile(G.toIndex([-1, -1, 0])))
print("[., ., 1]:", G.toProfile(G.toIndex([-1, -1, 1])))
print()

print("0:", G.toIndex(G.toProfile(0)))
print("1:", G.toIndex(G.toProfile(1)))

print("\nH tests:")
print("0:", H.toIndex(H.toProfile(0)))
print("1:", H.toIndex(H.toProfile(1)))
print("2:", H.toIndex(H.toProfile(2)))
print("3:", H.toIndex(H.toProfile(3)))
print("4:", H.toIndex(H.toProfile(4)))
print("5:", H.toIndex(H.toProfile(5)))
print("6:", H.toIndex(H.toProfile(6)))
print()

print("[., ., 0, 0, 0]:", H.toProfile(H.toIndex([-1, -1, 0, 0, 0])))
print("[., ., 1, 0, 0]:", H.toProfile(H.toIndex([-1, -1, 1, 0, 0])))
print("[., ., 2, 0, 0]:", H.toProfile(H.toIndex([-1, -1, 2, 0, 0])))
print("[., ., 0, 1, 0]:", H.toProfile(H.toIndex([-1, -1, 0, 1, 0])))
print("[., ., 0, 2, 0]:", H.toProfile(H.toIndex([-1, -1, 0, 2, 0])))
print("[., ., 0, 0, 1]:", H.toProfile(H.toIndex([-1, -1, 0, 0, 1])))
print("[., ., 0, 0, 2]:", H.toProfile(H.toIndex([-1, -1, 0, 0, 2])))