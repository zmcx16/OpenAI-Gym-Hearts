import random
from datetime import datetime

class RandomAI:
    def __init__(self, name, params = None):
        random.seed(datetime.now())
        self.name = name
        
        if params != None:
            self.print_info = params['print_info']
        else:
            self.print_info = False
    
    def Do_Action(self, observation):
        if observation['event_name'] == 'GameStart':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'NewRound':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'PassCards':
            if self.print_info:
                print(observation)
            
            passCards = random.sample(observation['data']['hand'],3)
            
            if self.print_info:
                print(self.name, ' pass cards: ', passCards)
                
            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name, 
                        'action': {'passCards': passCards}
                    }
                }
        
        elif observation['event_name'] == 'ShowPlayerHand':
            if self.print_info:
                print(observation)
        
        elif observation['event_name'] == 'PlayTrick':
            if self.print_info:
                print(observation)
            
            hand = observation['data']['hand']
            if '2c' in hand:
                choose_card = '2c'
            else:
                choose_card = random.choice(observation['data']['hand'])
                if self.print_info:
                    print(self.name, ' choose card: ', choose_card)

            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name, 
                        'action': {'card': choose_card}
                    }
                }            
        elif observation['event_name'] == 'ShowTrickAction':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'ShowTrickEnd':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'RoundEnd':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'GameOver':
            if self.print_info:
                print(observation)            