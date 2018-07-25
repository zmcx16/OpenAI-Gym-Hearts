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


env.render()

terminal = False
while not terminal:

    observation, info = env.request_action()
    
    now_event = observation['event_name']
    IsBroadcast = observation['broadcast']
    
    if IsBroadcast == True:
        for agent in agent_list:
            agent.Do_Action(observation)
    else:
        playName = observation['data']['playerName']
        for agent in agent_list:
            if agent.name == playName:
                action = agent.Do_Action(observation)    
                env.step({'event_name': now_event, 'data': {'playerName': playName, 'action': action}})
    
    """
    now_event = observation['event_name']
    now_hands = observation['event_data']['hand']
    print("ddd")
    print(now_hands)
    #env.step({'event_name': now_event, 'event_data': {'playerName': 'Kazuma', 'passCards': [now_hands[0],now_hands[1],now_hands[2]]}})
    """

"""
env.render()

terminal = False
while not terminal:
  # play safe actions, check when noone else has raised, call when raised.
  actions = holdem.safe_actions(community_infos, n_seats=n_seats)
  (player_states, (community_infos, community_cards)), rews, terminal, info = env.step(actions)
  env.render(mode='human')
"""
