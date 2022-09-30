from copy import deepcopy


class Player:
    def __init__(self, name, brute=False):
        self.name = name
        self.hand = []
        self.won = []
        self.round = 0
        self.board = 0
        self.brute = brute


    def __str__(self):
        rs = "  Name:" + self.name
        rs = rs + "\n  Cards won:"
        for w in self.won:
            rs += " " + str(w)
        rs = rs + "\n  Hand:"
        for c in self.hand:
            rs = rs +"  "+ str(c)
        return rs
    
    def assign(self, board):
        self.board = board
    
    def addCardToHand(self, card):
        self.hand.append(card)

    def addCardToHandSorted(self, card, bseed=""):
        if bseed == "" : bseed = self.board.briscola.seed
        self.hand.append(card)
        self.hand.sort(key = lambda x: (0 if x.seed==bseed else 1, x.seed, x.number))
    
    def addWonCard(self, cards): #pool of cards from the rounds the player has won
        self.won.append(cards)
     
    def play(self, cardN=0): #removes a card from the player's hand
        return self.hand.pop(cardN)
     
    def aPlay(self):
        move = 0
        if(self.brute):
            board = deepcopy(self.board)
            board.dumbPlayers()
            move = self.minimax(board, min(3, self.board.remainingHands()), [-100, 0], [100, 0], True)[1]
        return self.play(move)
    
    def played(self, round): #updates the round that the player has played(so that it matches with the board's when it has already played)
        self.round = round
    
    def getRound(self): #returns the number of the last round played
        return self.round
    
    def needsToDraw(self):
        return len(self.hand) < 3

    def getPoints(self) :
        p=0
        for c in self.won :
            p+=c.pointValue()
        return p

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.empty:
            d = board.twoPlayerEval()
            return [d, 0]
            
        if maximizingPlayer :
            maxEval = [-100, 0]
            for i in range(len(self.hand)):
                board = deepcopy(board)
                board.dumbPlayers()
                board.nextHand()
                eval = self.minimax(board, depth-1, alpha, beta, False)
                if eval[0] > maxEval[0]:
                    maxEval = [eval[0], i]
                if eval[0] > alpha[0]:
                    alpha = [eval[0], i]
                if beta[0] <= alpha[0]:
                    break
            return maxEval
        else:
            minEval = [100, 0]
            for i in range(len(self.hand)):
                board = deepcopy(board)
                board.dumbPlayers()
                board.nextHand()
                eval = self.minimax(board, depth-1, alpha, beta, True)
                if eval[0] < minEval[0]:
                    minEval = [eval[0], i]
                if eval[0] < beta[0]:
                    beta = [eval[0], i]
                if beta[0] >= alpha[0]:
                    break
            return minEval