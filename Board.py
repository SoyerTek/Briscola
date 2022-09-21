import random

class Card:
    def __init__(self, seed, number):
        self.seed = seed# 1 to 10 Asso, 2 ... 7, Fante, Cavallo, Re
        self.number = number# B_astoni, C_oppe, D_enare, S_pade
    
    def __str__(self):
        return self.seed + str(self.number)
    
    def greater(self, card): #returns FALSE if the seeds are different, or the best card 
        if self.seed != card.seed: return False
        if self.number == 1: return self
        if card.number == 1: return card
        if self.number == 3: return self
        if card.number == 3: return card
        if self.number > card.number: return self;
        return card
    
    def pointValue(self):
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
        self.firstPlayer = 0
        self.currentPlayer = 0
        self.empty = False
               
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
        self.cards = []
        for s in ["B", "C", "D", "S"]: 
            for x in range(1, 11):
                self.cards.append(Card(s, x))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)
    
    def addPlayer(self, player):
        self.players.append(player)

    def firstDeal(self):
        for x in range(3) :      
            for p in self.players :
                p.addCardToHand(self.cards.pop())
        self.briscola = self.cards.pop()


    def deal(self):
        if self.empty == 0 : 
            if len(self.cards) > 0 :
                for p in self.players :
                    if len(self.cards) > 0 :
                        c = self.cards.pop()
                        p.addCardToHandSorted(c, self.briscola.seed)
                    else:
                        p.addCardToHandSorted(self.briscola, self.briscola.seed)
                        self.empty += 1
        else: self.empty += 1
        
                
                
    def playHand(self):
        for p in self.players :
            self.tableCards.append({"card":p.play(), "player":p})
        winner = self.findHandWinner()
        #set the player who has won as the first player of the next hand
        i=0
        for i in range(0, len(self.players)):
            if self.players[(self.firstPlayer+i)%len(self.players)] != winner["player"] : continue
            else: break
        self.firstPlayer = (self.firstPlayer + i ) % len(self.players)
        self.deal()
        self.round = self.round + 1
        
    def playOne(self, cardN=0):
        cp = self.currentPlayer % len(self.players)
        self.currentPlayer += 1
        self.tableCards.append({"card":self.players[cp].play(cardN), "player":self.players[cp]})
        if cp != 0 and self.currentPlayer > 1 :
            if self.findHandWinner()["player"] != self.players[cp]: 
                self.currentPlayer+=1
                print("havintolaltro")
            self.deal()
            self.round = self.round + 1
                
    def twoPlayerEval(self) :
        return self.players[0].getPoints() - self.players[1].getPoints()
    
    def getCurrentPlayerHand(self):
        return self.players[self.currentPlayer%len(self.players)].hand