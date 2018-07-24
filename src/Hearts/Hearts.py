from .Deck import Deck
from .Card import Card, Suit, Rank
from .Player import Player
from .Trick import Trick

'''
Change auto to False if you would like to play the game manually.
This allows you to make all passes, and plays for all four players.
When auto is True, passing is disabled and the computer plays the
game by "guess and check", randomly trying moves until it finds a
valid one.
'''
auto = False
totalTricks = 13

queen = 12
noSuit = 0
spades = 2
hearts = 3
cardsToPass = 3


class Hearts:

    def __init__(self, playersName, maxScore=100):
        
        self.maxScore = maxScore
        
        self.roundNum = 0
        self.trickNum = 0  # initialization value such that first round is round 0
        self.dealer = -1  # so that first dealer is 0
        self.passes = [1, -1, 2, 0]  # left, right, across, no pass
        self.currentTrick = Trick()
        self.trickWinner = -1
        self.heartsBroken = False
        self.losingPlayer = None
        self.passingCards = [[], [], [], []]

        # Make four players

        self.players = [Player(playersName[0]), Player(playersName[1]), Player(playersName[2]), Player(playersName[3])]

        '''
        Player physical locations:
        Game runs clockwise

            p3
        p2        p4
            p1

        '''
        
        self.event = None
        
        # Generate a full deck of cards and shuffle it
        self.newRound()

    def handleScoring(self):
        p, highestScore = None, 0
        print ("\nScores:\n")
        for player in self.players:
            print (player.name + ": " + str(player.score))
            if player.score > highestScore:
                p = player
                highestScore = player.score
            self.losingPlayer = p
    
    def handsToStrList(self, hands):
        output = []
        for card in hands:
            output += [str(card)]
        return output
    
    def newRound(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.roundNum += 1
        self.trickNum = 0
        self.trickWinner = -1
        self.heartsBroken = False
        self.dealer = (self.dealer + 1) % len(self.players)
        self.dealCards()
        self.currentTrick = Trick()
        self.passingCards = [[], [], [], []]
        for p in self.players:
            p.discardTricks()
        
        self.event = 'PassCards'
        self.event_data_for_server = {'now_player_index': 0}
        self.event_data_for_client = {'playerName': self.players[0].name, 'hand': self.handsToStrList(sum(self.players[0].hand.hand, []))}

    def getFirstTrickStarter(self):
        for i, p in enumerate(self.players):
            if p.hand.contains2ofclubs:
                self.trickWinner = i

    def dealCards(self):
        i = 0
        while(self.deck.size() > 0):
            self.players[i % len(self.players)].addCard(self.deck.deal())
            i += 1

    def evaluateTrick(self):
        self.trickWinner = self.currentTrick.winner
        p = self.players[self.trickWinner]
        p.trickWon(self.currentTrick)
        self.printCurrentTrick()
        print (p.name + " won the trick.")
        # print 'Making new trick'
        self.currentTrick = Trick()
        print (self.currentTrick.suit)

    def passCards(self, index, action_data):
        print (action_data['event_data']['passCards'])
        passTo = self.passes[self.trickNum]  # how far to pass cards
        passTo = (index + passTo) % len(self.players)  # the index to which cards are passed
        
        passCard = self.players[index].play(action_data['event_data']['passCards'][0])
        self.passingCards[passTo].append(passCard)
        self.players[index].removeCard(passCard)
        passCard = self.players[index].play(action_data['event_data']['passCards'][1])
        self.passingCards[passTo].append(passCard)
        self.players[index].removeCard(passCard)
        passCard = self.players[index].play(action_data['event_data']['passCards'][2])
        self.passingCards[passTo].append(passCard)
        self.players[index].removeCard(passCard)
        
        print('now ', self.players[index].name, 'cards: ', self.players[index].hand)
        
    def distributePassedCards(self):
        for i, passed in enumerate(self.passingCards):
            for card in passed:
                self.players[i].addCard(card)
        self.passingCards = [[], [], [], []]


    def playersPassCards(self, current_player_i, action_data):

        self.printPlayers()
        if not self.trickNum % 4 == 3:  # don't pass every fourth hand
            current_player_i = self.event_data_for_server['now_player_index']
            print  # spacing
            self.printPlayer(current_player_i)
            self.passCards(current_player_i % len(self.players), action_data)
            
            if self.event_data_for_server['now_player_index'] == 4:
                self.distributePassedCards()
                self.printPlayers()
                return True
        
        return False

    def playTrick(self, start):
        shift = 0
        if self.trickNum == 0:
            startPlayer = self.players[start]
            addCard = startPlayer.play(option = "play", c = '2c')
            startPlayer.removeCard(addCard)

            self.currentTrick.addCard(addCard, start)

            shift = 1  # alert game that first player has already played

        # have each player take their turn
        for i in range(start + shift, start + len(self.players)):
            self.printCurrentTrick()
            curPlayerIndex = i % len(self.players)
            self.printPlayer(curPlayerIndex)
            curPlayer = self.players[curPlayerIndex]
            addCard = None

            while addCard is None:  # wait until a valid card is passed

                addCard = curPlayer.play(auto = auto)  # change auto to False to play manually

                # the rules for what cards can be played
                # card set to None if it is found to be invalid
                if addCard is not None:

                    # if it is not the first trick and no cards have been played,
                    # set the first card played as the trick suit if it is not a heart
                    # or if hearts have been broken
                    if self.trickNum != 0 and self.currentTrick.cardsInTrick == 0:
                        if addCard.suit == Suit(hearts) and not self.heartsBroken:
                            # if player only has hearts but hearts have not been broken,
                            # player can play hearts
                            if not curPlayer.hasOnlyHearts():
                                print (curPlayer.hasOnlyHearts())
                                print (curPlayer.hand.__str__())
                                print ("Hearts have not been broken.")
                                addCard = None
                            else:
                                self.currentTrick.setTrickSuit(addCard)
                        else:
                            self.currentTrick.setTrickSuit(addCard)

                    # player tries to play off suit but has trick suit
                    if addCard is not None and addCard.suit != self.currentTrick.suit:
                        if curPlayer.hasSuit(self.currentTrick.suit):
                            print ("Must play the suit of the current trick.")
                            addCard = None
                        elif addCard.suit == Suit(hearts):
                            self.heartsBroken = True

                    if self.trickNum == 0:
                        if addCard is not None:
                            if addCard.suit == Suit(hearts):
                                print ("Hearts cannot be broken on the first hand.")
                                self.heartsBroken = False
                                addCard = None
                            elif addCard.suit == Suit(spades) and addCard.rank == Rank(queen):
                                print ("The queen of spades cannot be played on the first hand.")
                                addCard = None

                    if addCard is not None and self.currentTrick.suit == Suit(noSuit):
                        if addCard.suit == Suit(hearts) and not self.heartsBroken:
                            print ("Hearts not yet broken.")
                            addCard = None

                    if addCard is not None:
                        if addCard == Card(queen, spades):
                            self.heartsBroken = True
                        curPlayer.removeCard(addCard)

            self.currentTrick.addCard(addCard, curPlayerIndex)

        self.evaluateTrick()
        self.trickNum += 1

    # print player's hand
    def printPlayer(self, i):
        p = self.players[i]
        print (p.name + "'s hand: " + str(p.hand))

    # print all players' hands
    def printPlayers(self):
        for p in self.players:
            print (p.name + ": " + str(p.hand))

    # show cards played in current trick
    def printCurrentTrick(self):
        trickStr = '\nCurrent table:\n'
        trickStr += "Trick suit: " + self.currentTrick.suit.__str__() + "\n"
        for i, card in enumerate(self.currentTrick.trick):
            if self.currentTrick.trick[i] is not 0:
                trickStr += self.players[i].name + ": " + str(card) + "\n"
            else:
                trickStr += self.players[i].name + ": None\n"
        print (trickStr)

    def getWinner(self):
        minScore = 200  # impossibly high
        winner = None
        for p in self.players:
            if p.score < minScore:
                winner = p
                minScore = p.score
        return winner
    
    def render(self):
        pass
        #print("TODO render")
        #event = {'event_name': 'switch cards', 'playerName': 'Kazuma'}
    
    def step(self,action_data):
        observation, reward, done, info = None, None, None, None
        
        if action_data == None:
            observation = {'event_name': self.event, 'event_data': self.event_data_for_client}
            return observation, reward, done, info
        
        if self.event == 'PassCards':
            for current_player_i in range(len(self.players)):
                if self.players[current_player_i].name == action_data['event_data']['playerName']:
                    IsAllFinished = self.playersPassCards(current_player_i, action_data)
                    if IsAllFinished:
                        self.event = 'getFirstTrickStarter'
                    break
                
        elif self.event == 'getFirstTrickStarter':
            IsAllFinished = hearts.getFirstTrickStarter()
            if IsAllFinished:
                self.event = 'playTrick'
                
        elif self.event == 'playTrick':
            IsAllFinished = hearts.playTrick(hearts.trickWinner)
            if IsAllFinished:
                self.event = 'handleScoring'        
        
        elif self.event == 'handleScoring':
            IsAllFinished = hearts.handleScoring()
            if IsAllFinished:
                self.event = 'newRound'
                
        elif self.event == 'newRound':
            IsAllFinished = hearts.newRound()
            if IsAllFinished:
                if hearts.losingPlayer is None or hearts.losingPlayer.score < self.maxScore:
                    print ("over")
                    print (hearts.getWinner().name, "wins!")                    
                                           
        return observation, reward, done, info
    
def run_Heart(playersName, maxScore=100):
    
    hearts = Hearts(playersName, maxScore=100)

    # play until someone loses
    while hearts.losingPlayer is None or hearts.losingPlayer.score < maxScore:
        while hearts.trickNum < totalTricks:
            print ("Round", hearts.roundNum)
            if hearts.trickNum == 0:
                if not auto:
                    hearts.playersPassCards()
                hearts.getFirstTrickStarter()
            print ('\nPlaying trick number', hearts.trickNum + 1)
            hearts.playTrick(hearts.trickWinner)

        # tally scores
        hearts.handleScoring()

        # new round if no one has lost
        if hearts.losingPlayer.score < maxScore:
            print ("New round")
            hearts.newRound()

    print ("")
    print (hearts.getWinner().name, "wins!")
