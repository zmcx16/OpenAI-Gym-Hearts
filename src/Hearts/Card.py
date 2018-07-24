class Card:
    def __init__(self, rank, suit):
        self.rank = Rank(rank)
        self.suit = Suit(suit)

    def __lt__(self, other):
        return (self.rank < other.rank or (self.rank == other.rank and self.suit < other.suit))

    def __ge__(self, other):
        return not (self < other)

    def __gt__(self, other):
        return (self.rank > other.rank or (self.rank == other.rank and self.suit > other.suit))

    def __le__(self, other):
        return not (self > other)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return not (self == other)

    def rank(self):
        return self.rank

    def suit(self):
        return self.suit

    def __str__(self):
        return self.rank.__str__() + self.suit.__str__()

'''
Suit identification (iden)
0: clubs
1: diamonds
2: spades
3: hearts

The suit that leads is trump, aces are high
'''

class Suit:
    def __init__(self, iden):
        self.iden = iden
        self.string = ''
        suits = ["c", "d", "s", "h"]
        if iden == -1:
            self.string = "Unset"
        elif iden <= 3:
            self.string = suits[iden]
        else:
            print('Invalid card identifier')

    def __eq__(self, other):
        return self.iden == other.iden

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.iden < other.iden

    def __gt__(self, other):
        return self.iden > other.iden

    def __ge__(self, other):
        return not (self < other)

    def __le__(self, other):
        return not (self > other)

    def __str__(self):
        return self.string



'''
Ranks indicated by numbers 2-14, 2-Ace
Where ace is high and two is low
'''
class Rank:
    def __init__(self, rank):
        self.rank = rank
        self.string = ''

        strings = ["T", "J", "Q", "K", "A"]

        if rank >= 2 and rank <= 9:
            self.string = str(rank)
        elif rank >= 10 and rank <= 14:
            self.string = strings[rank - 10]
        else:
            print('Invalid rank identifier')

    def __lt__(self, other):
        return self.rank < other.rank

    def __ge__(self, other):
        return not (self < other)

    def __gt__(self, other):
        return self.rank > other.rank

    def __le__(self, other):
        return not (self > other)

    def __eq__(self, other):
        return self.rank == other.rank

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.string


