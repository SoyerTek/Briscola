import random

class Card:
    def __init__(self, seed, number):
        """
        seed = "B", "C", "D", "S"
        number = 1..10
        """
        self.seed = seed# 1 to 10 Asso, 2 ... 7, Fante, Cavallo, Re
        self.number = number# B_astoni, C_oppe, D_enare, S_pade
    
    def __str__(self):
        return self.seed + str(self.number)
    
    def greater(self, card): 
        """
        returns FALSE if the seeds are different, or returns the best card 
        """
        if self.seed != card.seed: return False
        if self.number == 1: return self
        if card.number == 1: return card
        if self.number == 3: return self
        if card.number == 3: return card
        if self.number > card.number: return self;
        return card
    
    def pointValue(self): 
        """
        returnrs the point value of the card
        """
        match self.number:
            case 1 : return 11
            case 3 : return 10
            case 8 : return 2
            case 9 : return 3
            case 10 : return 4
            case _ : return 0



class Board:
    def __init__(self):
        self.cards = []
        self.tableCards = []
        self.briscola = 0
        self.players = []
        self.round = 0
        self.empty = False
        self.nextPlayer = 0
               
    def __str__(self):
        rs = "Deck cards:\n"
        for c in self.cards:
            rs = rs + str(c)+", "
       
        rs = rs + "\nTableCards:\n"     
        for c in self.tableCards:
            rs = rs + str(c["card"])+" "+str(c["player"].name)+", " 
      
        rs = rs + "\nBriscola:" + str(self.briscola)   
        rs = rs + "\nRound:" + str(self.round)
        
        rs = rs + "\nPlayers:\n"
        for p in self.players:
            rs = rs + str(p)+"\n ---\n"      
        
        return rs;
      
    def findHandWinner(self):#TODO this could be a sort
        winner = self.tableCards[0];
        for i in range(1, len(self.tableCards)):
            test = winner["card"].greater(self.tableCards[i]["card"])
            if test != False :
                if test != winner["card"] : winner = self.tableCards[i]
            elif self.tableCards[i]["card"].seed == self.briscola.seed :
                winner = self.tableCards[i]
        #give the current cards of the table to the winner
        for c in self.tableCards:
            winner["player"].won += [c["card"]]
        self.tableCards = []
        return winner


    def setupDeck(self): 
        """
        initializes cards array and shuffles them 
        sets the briscola as the first card
        """
        self.cards = []
        for s in ["B", "C", "D", "S"]: 
            for x in range(1, 11):
                self.cards.append(Card(s, x))
        self.shuffle()        
        self.briscola = self.cards.pop()

    def shuffle(self): 
        """
        randomizes cards order
        """
        random.shuffle(self.cards)
    
    def addPlayer(self, player):
        self.players.append(player)
        player.assign(self)

    def firstDeal(self):
        """
        Gives all players 3 cards, chooses the briscola
        """
        for x in range(3) :      
            for p in self.players :
                p.addCardToHand(self.cards.pop())


    def deal(self):
        """
        Gives each player a card from the deck, if there are no more cards
        assign the player the briscola 
        deprecated
        """
        #if self.empty == 0 : 
         #   if len(self.cards) > 0 :
          #      for p in self.players :
           #         if len(self.cards) > 0 :
            #           c = self.cards.pop()
             #           p.addCardToHandSorted(c, self.briscola.seed)
             #       else:
              #          p.addCardToHandSorted(self.briscola, self.briscola.seed)
               #         self.empty += 1
       # else: self.empty += 1
        return 0

    def draw(self):
        """
        returns a card from the deck or
        returns the briscola as the last card
        """
        if not self.empty :
            if len(self.cards) > 0 :
                c = self.cards.pop()
                return c
            else :
                self.empty = True
                return self.briscola

        
    def nextHand(self):
        """
        For each player, draws if necessary 
        adds the player with it's card to the tableCards
        finds a winner
        """
        n_players = len(self.players)
        for i in range(n_players) :
            player = self.players[(self.nextPlayer+i)%n_players]
            if player.needsToDraw() and not self.empty : player.addCardToHandSorted(self.draw(), self.briscola.seed)
            self.tableCards.append({"player":player, "card":player.aPlay()})
        winner = self.findHandWinner()
        self.nextPlayer = self.players.index(winner["player"])

                
    def twoPlayerEval(self) :
        return self.players[0].getPoints() - self.players[1].getPoints()

    def remainingHands(self) :
        return int(len(self.cards)/len(self.players))
    
    def dumbPlayers(self) :
        for p in self.players :
            p.brute = False