from copy import deepcopy
import random
from typing import OrderedDict

from Card import Card
from Player import Player


class Board:
    def __init__(self, humanFriendly=False) -> None:
        """
            humanFriendly True=verbose. Defaults to False.
        """
        self._players = []
        self._deck = []
        self._briscola = 0
        self._empty = False #the state of the deck
        self._startingPlayer = 0
        self._havePlayed = 0 #number of players who have played in the current hand
        self._table = OrderedDict() #ordered dictionary Player:card
        self._turns = 0
        self._humanFriendly = humanFriendly

        self.setupDeck()

    def setFriendlyness(self, f):
        self._humanFriendly = f

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
        for seme in ["B", "C", "D", "S"]:
            for val in range(1, 11) :
                self._deck.append(Card(val, seme))
                
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
        """
            Adds to the player's hand a card from the deck or
            if the deck is empty the briscola(only once)
        """
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
            print("  "+player._name + " played "+str(self._table[player]) + " - [" + " ".join(map(str, player.hand))+"]")

        if self._havePlayed%len(self._players) == 0: #all players have played this round
            best : Card = list(self._table.values())[0]
            bestP : Player = list(self._table.keys())[0]
            bestVal = best.getValue()
            for player in self._table : #find the winner
                playerCard = self._table[player]
                val = playerCard.getValue() if playerCard.seed == best.seed else 0 #cards that aren't of the 'lead' seed always lose
                val = playerCard.getValue() * 100 if playerCard.seed == self._briscola.seed else val #the highest briscola always wins
                if val > bestVal :
                    bestVal = val
                    best = playerCard
                    bestP = player
            bestP.addCardWon(list(self._table.values()))
            self._startingPlayer = self._players.index(bestP) #winner starts next hand
            self._havePlayed = 0 #reset the number of players who have already played
            self._table = OrderedDict()
            
            if self._humanFriendly:
                print(" "+bestP._name + " wins this hand.")
            
            for i in range(len(self._players)):
                player = self._players[(self._startingPlayer + i)%len(self._players)] #the winner/starting player draws first
                if player.needsToDraw:
                    self.draw(player)
    
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
                    
