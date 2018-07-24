from .Card import Card

'''
Tests different cards for (in)equality using a
unit test like format. Shows correctness of the operators,
which compare cards relative to each others' ranks.
'''

print('Starting Card opertor tests...\n')

clubs = 0
diamonds = 1
spades = 2
hearts = 3


# c = Card(2, hearts)
# c1 = Card(13, spades)

# print 'c:', c
# print 'c1:', c1

# print "c == c1", c == c1
# print "c >= c1", c >= c1
# print "c <= c1", c <= c1
# print "c < c1", c < c1
# print "c > c1", c > c1

# c = Card(12, diamonds)
# c1 = Card(7, clubs)

# print '\nc:', c
# print 'c1:', c1

# print "c == c1", c == c1
# print "c >= c1", c >= c1
# print "c <= c1", c <= c1
# print "c < c1", c < c1
# print "c > c1", c > c1


c = Card(12, diamonds)
c1 = Card(12, clubs)


print('\nc:', c)
print('c1:', c1)

print("c == c1", c == c1)
print("c >= c1", c >= c1)
print("c <= c1", c <= c1)
print("c < c1", c < c1)
print("c > c1", c > c1)

