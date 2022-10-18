from abc import abstractmethod
from math import floor
from random import randrange


class Strategy :
    @abstractmethod
    def move(self, board): pass
    
    def __str__(self) -> str:
        return self.__class__.__name__

class MiniMaxStrategy(Strategy):
    """
    Builds a tree of all possible moves from the current board onwords
    and chooses the best one for the current player
    """
    def move(self, board):
        return super().move()

class DefaultStrategy(Strategy):
    """
    Selects the first possible move
    """
    def move(self, board=0):
        return 0

class PrbabilityStrategy(Strategy):
    """
    Choses a move based on probability of it winning, based on drawn cards, previous hands, etc..
    """
    def move(self, board):
        return super().move()
    
class SimpleStrategyV4(Strategy):
    """
    Choses a move based on very simple rules:
    uses the lowest card of the same seed that will win
    or the lowest briscola
    or the card with the lowest value
    """
    def move(self, board):
        hand = board.currentPlayer.hand
        if len(board.table)==0 : #if it's the first player chooses random card
            x = sorted(hand, key=lambda x: x.number*10 if x.seed==board.briscola.seed else x.number, reverse=True)
            return hand.index(x[len(x)-1])
        else : #otherwise try to win with the lowest option
            firstCard = list(board.table.values())[0]
            lowestBriscola=-1
            lowestFirst=-1#the card with wich the turn started
            lowestGeneral=-1
            i=0
            for card in hand:
                lowestGeneral = i if lowestGeneral==-1 or card.compare(hand[lowestGeneral]) < 0 else lowestGeneral
                if card.seed == firstCard.seed :
                    if card.compare(firstCard) > 0 :
                        if lowestFirst == -1 or card.compare(hand[lowestFirst]) < 0:
                            lowestFirst = i
                if card.seed == board.briscola.seed :
                    lowestBriscola = i if lowestBriscola==-1 or card.compare(hand[lowestBriscola]) < 0 else lowestBriscola
                i+=1

            if lowestFirst != -1 : 
                return lowestFirst
            elif lowestBriscola != -1 and firstCard.seed != board.briscola.seed:
                return lowestBriscola
            else: 
                return lowestGeneral
    
class SimpleStrategyV3(Strategy):
    """
    Choses a move based on very simple rules:
    uses the lowest card of the same seed that will win
    or the lowest briscola
    or the card with the lowest value
    """
    def move(self, board):
        hand = board.currentPlayer.hand
        if len(board.table)==0 : #if it's the first player chooses random card
            x = sorted(hand, key=lambda x: x.number*10 if x.seed==board.briscola.seed else x.number, reverse=True)
            return hand.index(x[0])
        else : #otherwise try to win with the lowest option
            firstCard = list(board.table.values())[0]
            lowestBriscola=-1
            lowestFirst=-1#the card with wich the turn started
            lowestGeneral=-1
            i=0
            for card in hand:
                lowestGeneral = i if lowestGeneral==-1 or card.compare(hand[lowestGeneral]) < 0 else lowestGeneral
                if card.seed == firstCard.seed :
                    if card.compare(firstCard) > 0 :
                        if lowestFirst == -1 or card.compare(hand[lowestFirst]) < 0:
                            lowestFirst = i
                if card.seed == board.briscola.seed :
                    lowestBriscola = i if lowestBriscola==-1 or card.compare(hand[lowestBriscola]) < 0 else lowestBriscola
                i+=1

            if lowestFirst != -1 : 
                return lowestFirst
            elif lowestBriscola != -1 and firstCard.seed != board.briscola.seed:
                return lowestBriscola
            else: 
                return lowestGeneral
    
class SimpleStrategyV2(Strategy):
    """
    Choses a move based on very simple rules:
    uses the lowest card of the same seed that will win
    or the lowest briscola
    or the card with the lowest value
    """
    def move(self, board):
        hand = board.currentPlayer.hand
        if len(board.table)==0 : #if it's the first player chooses random card
            x = sorted(hand, key=lambda x: x.number*10 if x.seed==board.briscola.seed else x.number, reverse=True)
            return hand.index(x[0 if len(x)==1 else 1])
        else : #otherwise try to win with the lowest option
            firstCard = list(board.table.values())[0]
            lowestBriscola=-1
            lowestFirst=-1#the card with wich the turn started
            lowestGeneral=-1
            i=0
            for card in hand:
                lowestGeneral = i if lowestGeneral==-1 or card.compare(hand[lowestGeneral]) < 0 else lowestGeneral
                if card.seed == firstCard.seed :
                    if card.compare(firstCard) > 0 :
                        if lowestFirst == -1 or card.compare(hand[lowestFirst]) < 0:
                            lowestFirst = i
                if card.seed == board.briscola.seed :
                    lowestBriscola = i if lowestBriscola==-1 or card.compare(hand[lowestBriscola]) < 0 else lowestBriscola
                i+=1

            if lowestFirst != -1 : 
                return lowestFirst
            elif lowestBriscola != -1 and firstCard.seed != board.briscola.seed:
                return lowestBriscola
            else: 
                return lowestGeneral
    
class SimpleStrategyV1(Strategy):
    """
    Choses a move based on very simple rules:
    uses the lowest card of the same seed that will win
    or the lowest briscola
    or the card with the lowest value
    """
    def move(self, board):
        if len(board.table)==0 : #if it's the first player chooses random card
            return 0
        else : #otherwise try to win with the lowest option
            lowestBriscola=-1
            lowestFirst=-1#the card with wich the turn started
            lowestGeneral=-1
            firstCard = list(board.table.values())[0]
            hand = board.currentPlayer.hand
            i=0
            for card in hand:
                lowestGeneral = i if lowestGeneral==-1 or card.compare(hand[lowestGeneral]) < 0 else lowestGeneral
                if card.seed == firstCard.seed :
                    if card.compare(firstCard) > 0 :
                        if lowestFirst == -1 or card.compare(hand[lowestFirst]) < 0:
                            lowestFirst = i
                if card.seed == board._briscola.seed :
                    lowestBriscola = i if lowestBriscola==-1 or card.compare(hand[lowestBriscola]) < 0 else lowestBriscola
                i+=1

            if lowestFirst != -1 : 
                return lowestFirst
            elif lowestBriscola != -1 and firstCard.seed != board.briscola.seed:
                return lowestBriscola
            else: 
                return lowestGeneral

class RandomStrategy(Strategy):
    """
    Choses a move randomly
    """
    def move(self, board):
        return randrange(board.currentPlayer.handLenght)