# pysimultaneous.py
# Author: Andrew Lounsbury
# Date: 3/10/24
# Description: a class for handling simultaneous games with n players, n >= 2

class Player:
    numStrats = 2
    
    def __init__(self,numStrats = 2):
        self.numStrats = numStrats

class simGame:
    numPlayers = 2
    numOutcomes = 4
    payoffMatrix = []
    
    players = []
    
    mixedEquilibria = []
    paretoPureEquilibria = []
    pureEquilibria = []
    
    def __init__(self, numPlayers=2, numStrats = [2, 2]):
        for i in range(numPlayers):
            p = Player(numStrats[i])
            self.players.append(p)
        
        self.numPlayers = numPlayers
        self.payoffMatrix = []
        return
    
G = simGame(2, [2, 2])