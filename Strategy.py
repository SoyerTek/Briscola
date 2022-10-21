from abc import abstractmethod
from copy import deepcopy
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
    
    def __init__(self, depth=3) -> None:
        self._maxDepth = depth

    def move(self, board):
        #if 
        c =  MiniMaxStrategy.miniMax(board, board.getPlayersTeam(board.currentPlayer),\
                                     self._maxDepth, [-1, -1000], [-1, 1000], True)[0]
        return c
    
    @staticmethod
    def miniMax(board, team, depth, alpha, beta, maximizingPlayer):
        #print("team" + str(team) + " depth: " +str(depth) + " alpha: "+ str(alpha)+" beta: "+ str(beta)+ " maxing: "+str(maximizingPlayer))
        """
        returns index points
        """
        if board.isGameOver or depth==0:
            #print("val: "+str(board.pointsEval(team)))
            return [-1, board.pointsEval(team)]#tmpIndex, pointEval
        
        if maximizingPlayer:
            maxEval = [-1, -1000]
            for i in range(len(board.currentPlayer.hand)):
                boardCopy = deepcopy(board)
                boardCopy.setFriendlyness(False)
                #boardCopy.overrideStrategy(MiniMaxStrategy)#Likely to be unnecessary
                boardCopy.nextPlay(i)
                eval = MiniMaxStrategy.miniMax(boardCopy, team, depth-1, alpha, beta, False)
                eval[0] = i
                if eval[1] > maxEval[1]:
                    maxEval = eval
                if eval[1] > alpha[1]:
                    alpha = eval
                if beta[1] <= alpha[1]:
                    break
            return maxEval
        else:
            minEval = [-1, 1000]
            for i in range(len(board.currentPlayer.hand)):
                boardCopy = deepcopy(board)
                boardCopy.setFriendlyness(False)
                #boardCopy.overrideStrategy(MiniMaxStrategy)
                boardCopy.nextPlay(i)
                eval = MiniMaxStrategy.miniMax(boardCopy, team, depth-1, alpha, beta, True)
                eval[0] = i
                if eval[1] < minEval[1]:
                    minEval = eval
                if eval[1] < beta[1]:
                    beta = eval
                if beta[1] <= alpha[1]:
                    break
            return minEval   

    def __str__(self) -> str:
        return self.__class__.__name__+"("+str(self._maxDepth)+")"         

class HumanStrategy(Strategy):
    def move(self, board):
        if len(board.table)==0:
            print(" You are the first")
        else:
            print(" Cards on the table:")
            s ="  "
            for c in board.table.values():
                s+=str(c)+" "
            print(s)

        return HumanStrategy.cardInput(board.currentPlayer.hand)

    @staticmethod
    def cardInput(hand):
        s =" "
        for c in hand:
            s+=str(c)+" "
        print(" Your cards ["+s+"]")

        rs = -1
        while rs < 0 or rs > len(hand):
            cc = input(" Choose your card(0..2 or B1)")
            if len(cc) == 1:
                try:
                    rs = int(cc)
                except:
                    print(" Invalid input")
                    rs = -1
            elif len(cc) <= 3:
                i=0
                for c in hand:
                    if str(c).lower() == cc.lower():
                        rs = i
                        break
                    i+=1
                if rs==-1: print(" Invalid input")
            
        return rs



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
    
class SimpleStrategyV5(Strategy):
    """
    Choses a move based on very simple rules:
    If first uses the card with the lowest value(briscole > others).
    Otherwise responds with the lowest card of the same seed that will win
    or the lowest briscola
    or the card with the lowest value
    if there are any points on the table
    """
    def move(self, board):
        hand = board.currentPlayer.hand
        if len(board.table)==0 : #if it's the first player chooses the card with the lowest value(briscole > others).
            x = sorted(hand, key=lambda x: x.number*10 if x.seed==board.briscola.seed else x.number, reverse=True)
            return hand.index(x[len(x)-1])
        else : #otherwise try to win any points with the lowest option 
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
            
            tablePoints = 0
            for c in board.table.values():
                tablePoints+=c.getPointsValue()
            if tablePoints == 0:
                print("nopoint")
                return lowestGeneral
            if lowestFirst != -1 : 
                return lowestFirst
            elif lowestBriscola != -1 and firstCard.seed != board.briscola.seed:
                return lowestBriscola
            else: 
                return lowestGeneral

     
class SimpleStrategyV2(Strategy):
    """
    Choses a move based on very simple rules:
    If first uses the card with the median value(briscole > others).
    Otherwise responds with the lowest card of the same seed that will win
    or the lowest briscola
    or the card with the lowest value
    """
    #As p1 Wins decisively against SimpleStrategyV1,V3,V4
    #As p2 loses
    def move(self, board):
        hand = board.currentPlayer.hand
        if len(board.table)==0 : #if it's the first player chooses the card with the median value(briscole > others).
            x = sorted(hand, key=lambda x: x.number*10 if x.seed==board.briscola.seed else x.number, reverse=True)
            return hand.index(x[0 if len(x)==1 else 1])
        else : #otherwise try to win with the lowest option
            return SimpleStrategyV1().move(board)
    
class SimpleStrategyV1(Strategy):
    """
    Choses a move based on very simple rules:
    If first uses the card with the highest value(briscole > others).
    Otherwise responds with the lowest card of the same seed that will win
    or the lowest briscola
    or the card with the lowest value
    """
    #meh
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