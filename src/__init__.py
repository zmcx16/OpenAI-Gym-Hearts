from Hearts import *
from Agent import human

playersName = ['Kazuma', 'Aqua', 'Megumin', 'Darkness']
#run_Heart(playersName, maxScore=100)


agent_list = []
agent_list.append(human.Human('Kazuma'))
agent_list.append(human.Human('Aqua'))
agent_list.append(human.Human('Megumin'))
agent_list.append(human.Human('Darkness'))

env = Hearts([agent_list[0].name, agent_list[1].name, agent_list[2].name, agent_list[3].name], maxScore=100)

for i_episode in range(1):
    
    observation = env.reset()
    
    terminal = False
    while not terminal:

        now_event = observation['event_name']
        IsBroadcast = observation['broadcast']
        action = None
        if IsBroadcast == True:
            for agent in agent_list:
                agent.Do_Action(observation)
        else:
            playName = observation['data']['playerName']
            for agent in agent_list:
                if agent.name == playName:
                    action = agent.Do_Action(observation)    
           
        observation, reward, done, info = env.step(action) 
    

