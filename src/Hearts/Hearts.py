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
        self.round = 0

    def handleScoring(self):
              
        temp_score_list = [0, 0, 0, 0] 
        for current_player_i in range(len(self.players)):     
            heart_num = 0
            queen_spades = False   
            for card in self.players[current_player_i].CardsInRound:        
                if card.suit == Suit(hearts):
                    heart_num += 1
                elif card == Card(queen, spades):
                    queen_spades = True
            
            if heart_num == 13 and queen_spades == True:
                temp_score_list = [26,26,26,26]
                temp_score_list[current_player_i] = 0                
                break;
            else:
                temp_score_list[current_player_i] = heart_num + queen_spades*13
        
        for current_player_i in range(len(self.players)):
            self.players[current_player_i].score += temp_score_list[current_player_i]
    
    def handsToStrList(self, hands):
        output = []
        for card in hands:
            output += [str(card)]
        return output

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
        p.trickWon(self.currentTrick.trick)
        #self.printCurrentTrick()
        #print (p.name + " won the trick.")

    def passCards(self, index, action_data):
        #print (action_data['passCards'])
        passTo = self.passes[self.trickNum]  # how far to pass cards
        passTo = (index + passTo) % len(self.players)  # the index to which cards are passed
        
        passCard1 = self.players[index].play(action_data['passCards'][0])
        passCard2 = self.players[index].play(action_data['passCards'][1])
        passCard3 = self.players[index].play(action_data['passCards'][2])
        if passCard1 is not None and passCard2 is not None and passCard3 is not None:        
            self.passingCards[passTo].append(passCard1)
            self.players[index].removeCard(passCard1)
            self.passingCards[passTo].append(passCard2)
            self.players[index].removeCard(passCard2)
            self.passingCards[passTo].append(passCard3)
            self.players[index].removeCard(passCard3)       
            return True
        
        return False
        
    def distributePassedCards(self):
        for i, passed in enumerate(self.passingCards):
            for card in passed:
                self.players[i].addCard(card)
        self.passingCards = [[], [], [], []]


    def playersPassCards(self, current_player_i, action_data):

        self.printPlayers()
        if not self.trickNum % 4 == 3:  # don't pass every fourth hand

            self.printPlayer(current_player_i)
            if self.passCards(current_player_i % len(self.players), action_data) == True:
                self.event_data_for_server['now_player_index'] += 1
            
            if self.event_data_for_server['now_player_index'] == 4:
                self.distributePassedCards()
                self.printPlayers()
                return True
        
        return False


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
    
    def getCurrentTrickStrList(self):
        trick_list = []
        for i, card in enumerate(self.currentTrick.trick):
            if self.currentTrick.trick[i] is not 0:
                trick_list += [{'playerName': self.players[i].name, 'card': str(card) }]    
        
        return trick_list
        
    def getWinner(self):
        minScore = self.maxScore
        winner = None
        for p in self.players:
            if p.score < minScore:
                winner = p
                minScore = p.score
        return winner
    
    def reset(self):
        
        # Generate a full deck of cards and shuffle it     
        self.event = 'GameStart'        
        self._event_GameStart()
        observation = self.event_data_for_client
        self.event = 'NewRound'
        self.event_data_for_server = {}
        
        return observation
                
    def render(self):
        if self.event == 'show_event':
            pass
    
    def _event_GameStart(self):
        self.event_data_for_server = {}
        self.event_data_for_client \
        = {'event_name': self.event
           , 'broadcast': True
           , 'data': {
               "players" : [
                   {'playerName': self.players[0].name},
                   {'playerName': self.players[1].name},
                   {'playerName': self.players[2].name},
                   {'playerName': self.players[3].name}
                   ]
               }
           }
        
        for p in self.players:        
            p.score = 0
        self.round = 0
    
    def _event_NewRound(self):

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
        self.round += 1
        for p in self.players:
            p.resetRoundCards()
            p.discardTricks()

        self.event_data_for_client \
        = {'event_name': self.event
           , 'broadcast': True
           , 'data': {
               "players" : [
                   {'playerName': self.players[0].name,
                    'score': self.players[0].score},
                   {'playerName': self.players[1].name,
                    'score': self.players[1].score},
                   {'playerName': self.players[2].name,
                    'score': self.players[2].score},
                   {'playerName': self.players[3].name,
                    'score': self.players[3].score}
                   ]
               }
           }
        
        self.event = 'PassCards'
        self.event_data_for_server = {'now_player_index': 0}          

    def _event_PassCards(self, action_data):

        IsAllFinished = False           
        if action_data != None and action_data['event_name'] == "PassCards_Action":
            for current_player_i in range(len(self.players)):
                if self.players[current_player_i].name == action_data['data']['playerName']:
                    IsAllFinished = self.playersPassCards(current_player_i, action_data['data']['action'])                           
                    break
        
        if not IsAllFinished:
            now_player_index = self.event_data_for_server['now_player_index']
            self.event_data_for_client \
            =   {"event_name" : self.event,
                 "broadcast" : False,
                 "data" : {
                     'playerName': self.players[now_player_index].name, 
                     'hand': self.handsToStrList(sum(self.players[now_player_index].hand.hand, []))
                    }
                } 
        else:
            self.event = 'ShowPlayerHand'
            self.event_data_for_server = {'now_player_index': 0}
            self._event_ShowPlayerHand() 
    
    def _event_ShowPlayerHand(self):

        if self.event_data_for_server['now_player_index'] < 4:
            now_player_index = self.event_data_for_server['now_player_index']
            self.event_data_for_client \
            =   {"event_name" : self.event,
                 "broadcast" : False,
                 "data" : {
                     'playerName': self.players[now_player_index].name, 
                     'hand': self.handsToStrList(sum(self.players[now_player_index].hand.hand, []))
                    }
                }        
            self.event_data_for_server['now_player_index'] += 1
        
        else:
            self.event = 'PlayTrick'
            self.event_data_for_server = {'shift': 0}
            self._event_PlayTrick()
    
    def _event_PlayTrick(self):
                
        shift = self.event_data_for_server['shift']
        if self.trickNum == 0 and shift == 0:  
            self.getFirstTrickStarter()
            current_player = self.players[self.trickWinner]
            
        else:
            current_player_i = (self.trickWinner + shift)%4
            current_player = self.players[current_player_i] 
            
        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : False,
                "data" : {
                    'playerName': current_player.name, 
                    'hand': self.handsToStrList(sum(current_player.hand.hand, [])),
                    'trickNum': self.trickNum+1,
                    'trickSuit': self.currentTrick.suit.__str__(),
                    'currentTrick': self.getCurrentTrickStrList(),
                    'IsHeartsBroken': self.heartsBroken
                }
            }

    def _event_PlayTrick_Action(self, action_data):
        
        shift = self.event_data_for_server['shift']
        current_player_i = (self.trickWinner + shift)%4
        current_player = self.players[current_player_i]
        if self.trickNum == 0 and shift == 0:  
            if action_data['data']['action']['card'] == '2c':
                addCard = current_player.play('2c')
                current_player.removeCard(addCard)
                self.currentTrick.addCard(addCard, self.trickWinner)
                self.event_data_for_server['shift'] += 1
                
                self.event = 'ShowTrickAction'
                self._event_ShowTrickAction()
            else:
                self.event = 'PlayTrick'
                self._event_PlayTrick()
        else:
            
            addCard = current_player.play(action_data['data']['action']['card'])
            if addCard is not None:
                # if it is not the first trick and no cards have been played,
                # set the first card played as the trick suit if it is not a heart
                # or if hearts have been broken
                if self.trickNum != 0 and self.currentTrick.cardsInTrick == 0:
                    if addCard.suit == Suit(hearts) and not self.heartsBroken:
                        # if player only has hearts but hearts have not been broken,
                        # player can play hearts
                        if not current_player.hasOnlyHearts():
                            print (current_player.hasOnlyHearts())
                            print (current_player.hand.__str__())
                            print ("Hearts have not been broken.")
                            addCard = None
                        else:
                            self.currentTrick.setTrickSuit(addCard)
                    else:
                        self.currentTrick.setTrickSuit(addCard)

                # player tries to play off suit but has trick suit
                if addCard is not None and addCard.suit != self.currentTrick.suit:
                    if current_player.hasSuit(self.currentTrick.suit):
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
                    current_player.removeCard(addCard)
                    self.currentTrick.addCard(addCard, current_player_i)
                    self.event_data_for_server['shift'] += 1
                    self.event = 'ShowTrickAction'
                    self._event_ShowTrickAction()
                else:
                    self.event = 'PlayTrick'
                    self._event_PlayTrick()
                  
            
    def _event_ShowTrickAction(self):
        
        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : True,
                "data" : {
                    'trickNum': self.trickNum+1,
                    'trickSuit': self.currentTrick.suit.__str__(),
                    'currentTrick': self.getCurrentTrickStrList(),
                    'IsHeartsBroken': self.heartsBroken
                }
            }
        
        if self.currentTrick.cardsInTrick < 4:
            self.event = 'PlayTrick'
        else:
            self.event = 'ShowTrickEnd'
    
    def _event_ShowTrickEnd(self):
        
        self.evaluateTrick()
        
        cards = []
        for card in self.currentTrick.trick:
            cards += [str(card)]         
                 
        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : True,
                "data" : {
                    'trickNum': self.trickNum+1,
                    'trickWinner': self.players[self.trickWinner].name,
                    'cards': cards,
                    'IsHeartsBroken': self.heartsBroken
                }
            }
        
        self.currentTrick = Trick()
             
        self.trickNum += 1        
        if self.trickNum < 13:
            self.event = 'PlayTrick'
            self.event_data_for_server = {'shift': 0, 'IsHeartsBroken': self.heartsBroken}
        else:
            self.event = 'RoundEnd'
            self.event_data_for_server = {}
    
    def _event_RoundEnd(self):

        self.handleScoring()

        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : True,
                "data" : {
                    "players" : [
                       {'playerName': self.players[0].name,
                        'score': self.players[0].score},
                       {'playerName': self.players[1].name,
                        'score': self.players[1].score},
                       {'playerName': self.players[2].name,
                        'score': self.players[2].score},
                       {'playerName': self.players[3].name,
                        'score': self.players[3].score}
                       ],
                    'Round': self.round,
                }
            }
        
        
        temp_loser = max(self.players, key=lambda x:x.score)
        # new round if no one has lost
        if temp_loser.score < self.maxScore:
            self.event = 'NewRound'
            self.event_data_for_server = {}
        else:
            self.event = 'GameOver'
            self.event_data_for_server = {}
            
    def _event_GameOver(self):
        
        winner = min(self.players, key=lambda x:x.score)
        
        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : True,
                "data" : {
                    "players" : [
                        {'playerName': self.players[0].name,
                         'score': self.players[0].score},
                        {'playerName': self.players[1].name,
                         'score': self.players[1].score},
                        {'playerName': self.players[2].name,
                         'score': self.players[2].score},
                        {'playerName': self.players[3].name,
                         'score': self.players[3].score}
                        ],
                    'Round': self.round,
                    'Winner': winner.name
                }
            }
        
        self.event = None

    
    def step(self, action_data):
        observation, reward, done, info = None, None, None, None
            
        if self.event == 'NewRound':
            self._event_NewRound()
                       
        elif self.event == 'PassCards':
            self._event_PassCards(action_data)     
                      
        elif self.event == 'ShowPlayerHand':
            self._event_ShowPlayerHand()

        elif self.event == 'PlayTrick' or self.event == 'ShowTrickAction' or self.event == 'ShowTrickEnd':          
            if action_data != None and action_data['event_name'] == "PlayTrick_Action":
                self._event_PlayTrick_Action(action_data)            
            else:
                if self.event == 'PlayTrick':
                    self._event_PlayTrick()
                elif self.event == 'ShowTrickEnd':                    
                    self._event_ShowTrickEnd()
        
        elif self.event == 'RoundEnd':
            self._event_RoundEnd()
            
        elif self.event == 'GameOver':
            self._event_GameOver()              
        
        elif self.event == None:
            self.event_data_for_client = None
                                    
        
        observation = self.event_data_for_client                              
        return observation, reward, done, info
