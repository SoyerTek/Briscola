from audioop import minmax
from copy import deepcopy
from Board import Board
from Player import Player

def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.empty==3:
        d = board.twoPlayerEval()
        return [d, 0]
        
    if maximizingPlayer :
        maxEval = [-100, 0]
        print("croque"+ str(len(board.getCurrentPlayerHand())))
        for i in range(len(board.getCurrentPlayerHand())):
            board = deepcopy(board)
            board.players[board.currentPlayer%2].name += str(depth)
            board.playOne(i)
            eval = minimax(board, depth-1, alpha, beta, False)
            if eval[0] > maxEval[0]:
                maxEval = [eval[0], i]
            if eval[0] > alpha[0]:
                alpha = [eval[0], i]
            if beta[0] <= alpha[0]:
                break
        return maxEval
    else:
        minEval = [100, 0]
        print("croque" + str(len(board.getCurrentPlayerHand())))
        for i in range(len(board.getCurrentPlayerHand())):
            board = deepcopy(board)
            board.playOne(i)
            eval = minimax(board, depth-1, alpha, beta, True)
            if eval[0] < minEval[0]:
                minEval = [eval[0], i]
            if eval[0] < beta[0]:
                beta = [eval[0], i]
            if beta[0] >= alpha[0]:
                break
        return minEval
            
    

board = Board()
player1 = Player("mario")
player2 = Player("luigi")
player3 = Player("sandro")
player4 = Player("michele")

board.addPlayer(player1)
board.addPlayer(player2)
#board.addPlayer(player3)
#board.addPlayer(player4)
board.setupDeck()
board.firstDeal()

print(board)


for i in range(0, int(40)) :
    res = minimax(deepcopy(board), 3, [-100, 0], [100, 0], True)
    print("scrub" +str(res))
    board.playOne(res[1])
    if i%2==0 :
        print(board)
    #board.playHand()
    #print(board)
