from Hearts import *

playersName = ['Kazuma', 'Aqua', 'Megumin', 'Darkness']
#run_Heart(playersName, maxScore=100)

env = Hearts(playersName, maxScore=100)
env.render()

terminal = False
observation, reward, done, info = env.step(None)
print(observation)

now_event = observation['event_name']
now_hands = observation['event_data']['hand']
print("ddd")
print(now_hands)
env.step({'event_name': now_event, 'event_data': {'playerName': 'Kazuma', 'passCards': [now_hands[0],now_hands[1],now_hands[2]]}})


"""
env.render()

terminal = False
while not terminal:
  # play safe actions, check when noone else has raised, call when raised.
  actions = holdem.safe_actions(community_infos, n_seats=n_seats)
  (player_states, (community_infos, community_cards)), rews, terminal, info = env.step(actions)
  env.render(mode='human')
"""
