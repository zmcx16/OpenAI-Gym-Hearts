class Human:
    def __init__(self, name, params):
        self.name = name
    
    def Do_Action(self, observation):
        if observation['event_name'] == 'GameStart':
            print(observation)
        elif observation['event_name'] == 'NewRound':
            print(observation)
        elif observation['event_name'] == 'PassCards':
            print(observation)
            passCards = []
            for i in range(3):
                passCards.append(input('{0} pass card{1}: '.format(self.name, i+1)))
            
            print('passCards: ', passCards)
            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name, 
                        'action': {'passCards': passCards}
                    }
                }
        
        elif observation['event_name'] == 'ShowPlayerHand':
            print(observation)
        
        elif observation['event_name'] == 'PlayTrick':
            print(observation)
            
            hand = observation['data']['hand']
            if '2c' in hand:
                choose_card = '2c'
            else:
                choose_card = input('choose card: ')
            
            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name, 
                        'action': {'card': choose_card}
                    }
                }            
        elif observation['event_name'] == 'ShowTrickAction':
            print(observation)
        elif observation['event_name'] == 'ShowTrickEnd':
            print(observation)
        elif observation['event_name'] == 'RoundEnd':
            print(observation)
        elif observation['event_name'] == 'GameOver':
            print(observation)            