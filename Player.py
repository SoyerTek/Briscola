from Card import Card


class Player:
    def __init__(self, name, board, strategy=0) -> None:
        self.name = name
        self.board = board
        self.strategy = strategy
        self.hand = []
        self.cardsWon = []

        board.assignPlayer(self)

    def makeDumbMove(self, move=0) -> Card:
        """
        Returns hands[move]
        move=0..len(self.hand)
        """
        if move >= len(self.hand) :
             raise Exception("Player: There are " + str(len(self.hand)) +" cards, "+str(move) + " was requested")
        return self.hand.pop(move)

    def makeStrategicMove(self) -> Card:
        return self.makeDumbMove()

    def addCardToHand(self, card):
        """
        Adds a card to the players hand
        """
        if len(self.hand) >= 3 :
            raise Exception("Player " + self.name + " is trying to draw more than 3 cards")
        self.hand.append(card)
        #self.hand.sort(key = lambda x: (0 if x.seed==self.board.briscola.seed else 1, x.seed, x.number))