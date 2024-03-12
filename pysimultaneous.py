# pysimultaneous.py
# Author: Andrew Lounsbury
# Date: 3/10/24
# Description: a class for handling simultaneous games with n players, n >= 2

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
    
    def __init__(self, numPlayers = 2, numStrats = [2, 2]):
        for i in range(numPlayers):
            p = Player(numStrats[i])
            self.players.append(p)
        
        self.numPlayers = numPlayers
        self.payoffMatrix = []
        for i in range(self.players[0].numStrats):
            row = []
            for j in range(self.players[1].numStrats):
                row.append([0, 0])
            self.payoffMatrix.append(row)
                
        return
    
    def enterPayoffs(self, payoffs = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]):
        self.payoffMatrix = payoffs
    
    def printGame(self):
        for i in range(self.players[0].numStrats):
            for j in range(self.players[1].numStrats):
                for n in range(self.numPlayers):
                    if n < self.numPlayers - 1:
                        print(self.payoffMatrix[i][j][n], end=", ")
                    else:
                        print(self.payoffMatrix[i][j][n], end="")
                print(" ", end="")
            print()
            
G = simGame(2, [2, 2])
G.printGame()

newPayoffs = [[[-3, -3], [0, -5]], [[-5, 0], [-1, -1]]]

G.enterPayoffs(newPayoffs)
G.printGame()