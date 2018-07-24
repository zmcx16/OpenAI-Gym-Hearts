from .Card import Card, Suit

hearts = 3 # the corresponding index to the suit hearts
spades = 2
queen = 12

class Trick:
    def __init__(self):
        self.trick = [0, 0, 0, 0]
        self.suit = Suit(-1)
        self.cardsInTrick = 0
        self.points = 0
        self.highest = 0 # rank of the high trump suit card in hand
        self.winner = -1

    def reset(self):
        self.trick = [0, 0, 0, 0]
        self.suit = -1
        self.cardsInTrick = 0
        self.points = 0
        self.highest = 0
        self.winner = -1

    # def cardsInTrick(self):
    #     count = 0
    #     for card in self.trick:
    #         if card is not 0:
    #             count += 1
    #     return count

    def setTrickSuit(self, card):
        self.suit = card.suit

    def addCard(self, card, index):
        if self.cardsInTrick == 0: # if this is the first card added, set the trick suit
            self.setTrickSuit(card)
            print ('Current trick suit:', self.suit)
        
        self.trick[index] = card
        self.cardsInTrick += 1

        if card.suit == Suit(hearts):
            self.points += 1
        elif card == Card(queen, spades):
            self.points += 13

        if card.suit == self.suit:
            if card.rank.rank > self.highest:
                self.highest = card.rank.rank
                self.winner = index
                print ("Highest:",self.highest)
