class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.won = []
        self.round = 0


    def __str__(self):
        rs = "  Name:" + self.name
        rs = rs + "\n  Cards won:"
        for w in self.won:
            rs += " " + str(w)
        rs = rs + "\n  Hand:"
        for c in self.hand:
            rs = rs +"  "+ str(c)
        return rs
    
    
    def addCardToHand(self, card):
        self.hand.append(card)
        
        
    def addCardToHandSorted(self, card, bseed):
        self.hand.append(card)
        self.hand.sort(key = lambda x: (0 if x.seed==bseed else 1, x.seed, x.number))
    
    
    def addWonCard(self, cards): #pool of cards from the rounds the player has won
        self.won.append(cards)
    
    
    def play(self, cardN=0): #removes a card from the player's hand
        return self.hand.pop(cardN)
    
    
    def played(self, round): #updates the round that the player has played(so that it matches with the board's when it has already played)
        self.round = round
    
    
    def getRound(self): #returns the number of the last round played
        return self.round


    def getPoints(self) :
        p=0
        for c in self.won :
            p+=c.pointValue()
        return p