from Board import Board
from Player import Player


board = Board()
p1 = Player("Mario", board)
p2 = Player("Luigi", board)

for i in range(40):
    board.nextPlay()

print("test")
