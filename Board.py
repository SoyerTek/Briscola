import random
from typing import OrderedDict

from jellyfish import damerau_levenshtein_distance
from Card import Card
from Player import Player


class Board:
    def __init__(self) -> None:
        self.players = []
        self.deck = []
        self.briscola = 0
        self.empty = False#the state of the deck
        self.startingPlayer = 0
        self.havePlayed = 0#number of players who have played in the current hand
        self.table = OrderedDict() #ordered dictionary Player:card
        self.setupDeck()

    def setupDeck(self):
        for s in ["B", "C", "D", "S"]:
            for i in range(1, 11) :
                self.deck.append(Card(i, s))
        random.shuffle(self.deck)
        self.briscola = self.deck.pop()

    def assignPlayer(self, player):
        """
        Registers a player
        """
        self.players.append(player)
        for i in range(2):
            self.draw(player)

    def draw(self, player : Player):
        if not self.empty :
            if len(self.deck) > 0:
                player.addCardToHand(self.deck.pop())
            else:
                self.empty = True
                player.addCardToHand(self.briscola)

    def nextPlay(self):
        player = self.players[(self.startingPlayer + self.havePlayed)%len(self.players)]
        self.draw(player)
        self.table[player] = player.makeStrategicMove()
        self.havePlayed+=1

        if self.havePlayed%len(self.players) == 0: #all players have played
            best : Card = list(self.table.values())[0]
            bestP : Player = list(self.table.keys())[0]
            bestVal = best.getValue()
            for p in self.table :#find the winner
                pc = self.table[p]
                val = pc.getValue() if pc.seed == best.seed else 0
                val = pc.getValue() * 100 if pc.seed == self.briscola.seed else val
                if val > bestVal :
                    bestVal = val
                    best = pc
                    bestP = p
            print(list(self.table.values()))
            bestP.cardsWon.extend(list(self.table.values()))
            self.startingPlayer = self.players.index(bestP)#winner starts next hand
            self.havePlayed = 0 #reset the number of players who have already played
            self.table = OrderedDict()
                    
