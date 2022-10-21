
import bisect
from copy import deepcopy
from string import capwords
from Card import Card
from Strategy import DefaultStrategy, Strategy


class Player:
    def __init__(self, name, board, strategy=DefaultStrategy()) -> None:
        self._name = name
        self._board = board
        self._strategy = strategy
        self._hand = []
        self._cardsWon = []

        self._board.assignPlayer(self)

    @property
    def needsToDraw(self):
        return (len(self._hand) < 3)
        
    def getPoints(self) -> int:
        points = 0
        for c  in self._cardsWon:
            points += c.getPointsValue()
        return points

    def makeDumbMove(self, move=0) -> Card:
        """
        Returns hands[move]
        move=0..len(self.hand)
        """
        if move >= len(self._hand) :
             raise Exception("Player: There are " + str(len(self._hand)) +" cards, "+str(move) + " was requested")
        return self._hand.pop(move)

    def makeStrategicMove(self) -> Card:
        return self.makeDumbMove(self._strategy.move(self._board))

    def addCardToHand(self, card):
        """
        Adds a card to the players hand
        """
        if len(self._hand) >= 3 :
            raise Exception("Player " + self._name + " is trying to draw more than 3 cards")
        #self._hand.append(card)
        if len(self._hand) == 0:
            self._hand.append(card)
        else:
            for i in range(len(self.hand)):
                if self._hand[i].getValue() < card.getValue():
                    break
            self._hand[i:i] = [card]
        #self.hand.sort(key = lambda x: (0 if x.seed==self.board.briscola.seed else 1, x.seed, x.number))

    def addCardWon(self, cards):
        """
        appends the list cards to self.cardsWon
        """
        self._cardsWon.extend(cards)

    @property
    def handLenght(self):
        return len(self._hand)

    @property
    def hand(self):
        return deepcopy(self._hand)