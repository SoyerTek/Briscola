from Board import Board
from Player import Player
from Strategy import DefaultStrategy, SimpleStrategy

board = Board()
p1 = Player("Mario", board, DefaultStrategy())
p2 = Player("Luigi", board, SimpleStrategy())

for i in range(40):
    board.nextPlay()

print("ha vinto " + str(board.eval()))

