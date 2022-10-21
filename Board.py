from copy import deepcopy
import random
from typing import OrderedDict

from Card import Card
from Player import Player


class Board:
    def __init__(self, humanFriendly=False) -> None:
        self._players = []
        self._deck = []
        self._briscola = 0
        self._empty = False#the state of the deck
        self._startingPlayer = 0
        self._havePlayed = 0#number of players who have played in the current hand
        self._table = OrderedDict() #ordered dictionary Player:card
        self._turns = 0
        self._humanFriendly = humanFriendly

        self.setupDeck()

    @property
    def isGameOver(self):
        return self._turns==40

    @property
    def briscola(self) :
        return deepcopy(self._briscola)
    
    @property
    def currentPlayer(self) -> Player:
        return self._players[(self._startingPlayer + self._havePlayed)%len(self._players)]
    
    @property
    def table(self):
        return deepcopy(self._table)

    def setupDeck(self):
        for s in ["B", "C", "D", "S"]:
            for i in range(1, 11) :
                self._deck.append(Card(i, s))
        random.shuffle(self._deck)
        self._briscola = self._deck.pop()
        if self._humanFriendly :
            print("The briscola is: "+str(self._briscola))

    def assignPlayer(self, player):
        """
        Registers a player
        """
        self._players.append(player)
        for i in range(3):
            self.draw(player)

    def draw(self, player : Player):
        if not self._empty :
            if len(self._deck) > 0:
                player.addCardToHand(self._deck.pop())
            else:
                self._empty = True
                player.addCardToHand(self._briscola)

    def nextPlay(self, forcedMove=-1):
        player = self.currentPlayer
        self._table[player] = player.makeStrategicMove() if forcedMove==-1 \
                              else player.makeDumbMove(forcedMove)
        self._havePlayed+=1
        self._turns+=1
        if self._humanFriendly:
            print("  "+player._name + " played "+str(self._table[player]))

        if self._havePlayed%len(self._players) == 0: #all players have played
            best : Card = list(self._table.values())[0]
            bestP : Player = list(self._table.keys())[0]
            bestVal = best.getValue()
            for p in self._table :#find the winner
                pc = self._table[p]
                val = pc.getValue() if pc.seed == best.seed else 0
                val = pc.getValue() * 100 if pc.seed == self._briscola.seed else val
                if val > bestVal :
                    bestVal = val
                    best = pc
                    bestP = p
            bestP.addCardWon(list(self._table.values()))
            self._startingPlayer = self._players.index(bestP)#winner starts next hand
            self._havePlayed = 0 #reset the number of players who have already played
            self._table = OrderedDict()
            
            if self._humanFriendly:
                print(" "+bestP._name + " wins this hand.")
            
            for i in range(len(self._players)):
                p = self._players[(self._startingPlayer + i)%len(self._players)]
                if p.needsToDraw: #sadcheck
                    self.draw(p)
                else: print("pointless draw")#TODO remove
    
    def eval(self) -> int :
        w = 0
        i = 0
        max = 0
        for p in self._players:
            if max < p.getPoints() :
                max = p.getPoints()
                w=i
            i+=1
        return w%2

    def pointsEval(self, team=-1) :
        points = [0, 0]
        i = 0
        for p in self._players:
            points[i%2] += p.getPoints()
            i+=1
        if team==-1 :
            return points
        else:
            return points[team]
    
    def getPlayersTeam(self, player) -> int:
        return self._players.index(player) % 2
                    
