# pysimultaneous.py
# Author: Andrew Lounsbury
# Date: 3/10/24
# Description: a class for handling simultaneous games with n players, n >= 2

class simGame:
    numPlayers = 2
    numOutcomes = 4
    payoffMatrix
    
    mixedEquilibria
    paretoPureEquilibria
    pureEquilibria
    
    def __init__(self, numPlayers=2):
        self.numPlayers = numPlayers
        return