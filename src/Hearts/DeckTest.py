'''
Tests generation of a full 52 card Deck and that cards are
sorted by rank and then by suit within rank
'''

from .Deck import Deck

d = Deck()
print ('Deck size:',d.size())
d.shuffle()
print ('\nBefore sort:')
print (d)

d.sort()

print ('After sort:')
print (d)