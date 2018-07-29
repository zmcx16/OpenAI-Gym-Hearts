# OpenAI_Gym_Hearts_Card_Game
* Implement an OpenAI Gym Hearts Card Game simulation environment, easy to collect game data to use it in Machine Learning and Reinforcement Learning, the main game logic is fork from https://github.com/danielcorin/Hearts.

# Requirement
```
pip install gym
```

# Demo
```
python run_example.py
```

# Support Agent
* Human
* Random 

# Scoring
* Queen card is 1 penalty point, Queen of Spades is 13 penalty points.
* Shooting the moon: If one player takes all the penalty cards on one deal, that player's score remains unchanged while 26 penalty points are added to the scores of each of the other players.

# Game Flow
1.	env.reset() -> Start Hearts game, env send the GameStart event to all player.
2.	env send NewRound event to all player.
3.	env send PassCards event to each player, the player need choose 3 cards to pass other player and send PassCards_Action event to env.
4.	After all players send legal PassCards_Action event, env will send ShowPlayerHand event to each player to get the final hand cards.
5.  env send PlayTrick event to the player, the player choose a card and send PlayTrick_Action event to env.
6.  env will send ShowTrickAction event to all players to tell them the player's action.
7.  After all players take a card, env will send ShowTrickEnd event to tell the players that which one win this trick.
8.  After last trick, env will send RoundEnd event to announce which player win this round, if the loser's score > max_score, env send GameOver event to all players and exit the game, or send NewRound event to all players to continue game.

# API
* GameStart
```
{
    "event_name" : "GameStart",
    "broadcast" : True,
    "data" : {
        "players" : [
            {'playerName': 'Kazuma'},
            {'playerName': 'Aqua'},
            {'playerName': 'Megumin'},
            {'playerName': 'Darkness'}
        ]
    }

}
```

* NewRound
```
{
    "event_name" : "NewRound",
    "broadcast" : True,
    "data" : {
        "players" : [
            {'playerName': 'Kazuma'
            ,'score': 0},
            {'playerName': 'Aqua'
            ,'score': 0},
            {'playerName': 'Megumin'
            ,'score': 0},
            {'playerName': 'Darkness'
            ,'score': 0}
        ]
    }
}
```

* PassCards
```
{
    "event_name" : "PassCards",
    "broadcast" : False,
    "data" : {
        'playerName': 'Kazuma', 
        'hand': ['6c', '2d', '3d', '6d', '7d', 'Jd', 'Qd', '3s', '3h', '6h', 'Qh', 'Kh', 'Ah']
    }
}
```

* PassCards_Action
```
{
    "event_name" : "PassCards_Action",
    "data" : {
        'playerName': 'Kazuma', 
        'action': {'passCards': ['6c', '2d', '3d']}
    }
}
```

* ShowPlayerHand
```
{
    "event_name" : "ShowPlayerHand",
    "broadcast" : Fasle,
    "data" : {
        'playerName': 'Kazuma', 
        'hand': ['Ac', '6d', '7d', '9d', 'Jd', 'Qd', '3s', '3h', '6h', 'Jh', 'Qh', 'Kh', 'Ah']
    }
}
```

* PlayTrick
```
{
    "event_name" : "PlayTrick",
    "broadcast" : False,
    "data" : {
        'playerName': 'Kazuma', 
        'hand': ['7d', '9d', 'Jd', 'Qd', '3s', '3h', '6h', 'Jh', 'Qh', 'Kh', 'Ah'],
        'trickNum': 3,
        'trickSuit': 's',               //first player this value = "Unset"
        'currentTrick': [
            {'playerName': 'Megumin'
            ,'card': '9s'},
            {'playerName': 'Darkness'
            ,'card': '7s'}
		],
		'IsHeartsBroken': False
    }

}
```

* PlayTrick_Action
```
{
    "event_name" : "PlayTrick_Action",
    "data" : {
        'playerName': 'Kazuma', 
        'action': {'card': '3s'}
    }
}
```

* ShowTrickAction
```
{
    "event_name" : "ShowTrickAction",
    "broadcast" : True,
    "data" : {
        'trickNum': 3,
        'trickSuit': 'c',
        'currentTrick': [
            {'playerName': 'Kazuma'
            ,'card': '3s'},
            {'playerName': 'Megumin'
            ,'card': '9s'},
            {'playerName': 'Darkness'
            ,'card': '7s'}
		],
        'IsHeartsBroken': False
    }
}
```

* ShowTrickEnd
```
{
    "event_name" : "ShowTrickEnd",
    "broadcast" : True,
    "data" : {
        'trickNum': 3,
        'trickWinner': 'Megumin',
        'cards': ['3s', '2s', '9s', '7s'],
		'IsHeartsBroken': False
    }
}
```

* RoundEnd
```
{
    "event_name" : "RoundEnd",
    "broadcast" : True,
    "data" : {
        "players" : [
            {'playerName': 'Kazuma'
            ,'score': 10},
            {'playerName': 'Aqua'
            ,'score': 13},
            {'playerName': 'Megumin'
            ,'score': 3},
            {'playerName': 'Darkness'
            ,'score': 0}
        ],
		'ShootingMoon': False,
        'Round': 3
    }
}
```

* GameOver
```
{
    "event_name" : "GameOver",
    "broadcast" : True,
    "data" : {
        "players" : [
            {'playerName': 'Kazuma'
            ,'score': 0},
            {'playerName': 'Aqua'
            ,'score': 120},
            {'playerName': 'Megumin'
            ,'score': 36},
            {'playerName': 'Darkness'
            ,'score': 26}
        ],
        'Round': 7,
        'Winner': 'Kazuma'
    }
}
```

# Reference
* https://github.com/danielcorin/Hearts

# License
This project is licensed under the terms of the MIT license.