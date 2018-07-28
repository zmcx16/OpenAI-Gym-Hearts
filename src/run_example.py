from Hearts import *
from Agent.human import Human
from Agent.randomAI import RandomAI

playersName = ['Kazuma', 'Aqua', 'Megumin', 'Darkness']
#run_Heart(playersName, maxScore=100)


agent_list = []
agent_list.append(RandomAI('Kazuma', {'print_info': True}))
agent_list.append(RandomAI('Aqua', {'print_info': True}))
agent_list.append(RandomAI('Megumin', {'print_info': True}))
agent_list.append(RandomAI('Darkness', {'print_info': True}))

env = Hearts([agent_list[0].name, agent_list[1].name, agent_list[2].name, agent_list[3].name], maxScore=100)

for i_episode in range(10):
    
    observation = env.reset()
    
    while True:

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

        if observation == None:
            break
