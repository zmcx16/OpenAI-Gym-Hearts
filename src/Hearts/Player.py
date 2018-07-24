from .Hand import Hand

class Player:
    def __init__(self, name, auto=False):
            self.name = name
            self.hand = Hand()
            self.score = 0
            self.tricksWon = []

    def addCard(self, card):
        self.hand.addCard(card)


    def getInput(self, action_data):
        card = None
        while card is None:
            card = action_data
        return card

    def play(self, option='play', c=None, auto=False):
        if auto:
            card = self.hand.getRandomCard()
        elif c is None:
            card = self.getInput(option)
        else:
            card = c
        if not auto:
            card = self.hand.playCard(card)
        return card


    def trickWon(self, trick):
        self.score += trick.points


    def hasSuit(self, suit):
        return len(self.hand.hand[suit.iden]) > 0

    def removeCard(self, card):
        self.hand.removeCard(card)

    def discardTricks(self):
        self.tricksWon = []

    def hasOnlyHearts(self):
        return self.hand.hasOnlyHearts()