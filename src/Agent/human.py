class Human:
    def __init__(self, name):
        self.name = name
    
    def Do_Action(self, observation):
        print(observation)
        if observation['event_name'] == 'PassCards':
            passCards = []
            for i in range(3):
                passCards.append(input('pass card{0}: '.format(i+1)))
            
            print('passCards: ', passCards)
            return {'passCards': passCards}
        
        elif observation['event_name'] == 'showFinalHand':
            print(observation)
