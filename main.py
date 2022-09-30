from audioop import minmax
from copy import deepcopy
from Board import Board
from Player import Player       
    

board = Board()
player1 = Player("mario", False)
player2 = Player("luigi", True)
player3 = Player("sandro")
player4 = Player("michele")

board.addPlayer(player1)
board.addPlayer(player2)
#board.addPlayer(player3)
#board.addPlayer(player4)
board.setupDeck()
board.firstDeal()

print(board)


for i in range(0, int(40/len(board.players))):
    board.nextHand()
    print(board)