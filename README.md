# OpenAI_Gym_Hearts_Card_Game

# API
* GameStart
```
{
    "event_name" : "GameStart",
    "broadcast" : True,
    "RequestAction" : False,
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
    "RequestAction" : False,
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
    "RequestAction" : True,
    "data" : {
        'playerName': 'Kazuma', 
        'hand': ['ac', ...]
    }
}
```

* PassCards_Action
```
{
    "event_name" : "PassCards_Action",
    "data" : {
        'playerName': 'Kazuma', 
        'action': {'passCards': ['ac','kd','4s']}
    }
}
```

* ShowPlayerHand
```
{
    "event_name" : "ShowPlayerHand",
    "broadcast" : Fasle,
    "RequestAction" : False,
    "data" : {
        'playerName': 'Kazuma', 
        'hand': ['ac', ...]
    }
}
```

* PlayTrick
```
{
    "event_name" : "PlayTrick",
    "broadcast" : False,
    "RequestAction" : True,
    "data" : {
        'playerName': 'Kazuma', 
        'hand': ['ac', ...],
        'trickNum': 3,
        'trickSuit': 'c',               //first player this value = "Unset"
        'currentTrick': [
            {'playerName': 'Kazuma'
            ,'card': '3c'},
            {'playerName': 'Aqua'
            ,'card': None},
            {'playerName': 'Megumin'
            ,'card': None},
            {'playerName': 'Darkness'
            ,'card': None}
		]		
    }

}
```

* PlayTrick_Action
```
{
    "event_name" : "PlayTrick_Action",
    "data" : {
        'playerName': 'Kazuma', 
        'action': {'card': '3c'}
    }
}
```

* ShowTrickAction
```
{
    "event_name" : "ShowTrickAction",
    "broadcast" : True,
    "RequestAction" : False,
    "data" : {
        "players" : [
            {'playerName': 'Kazuma'
            ,'card': None},
            {'playerName': 'Aqua'
            ,'card': '4c'},
            {'playerName': 'Megumin'
            ,'card': None},
            {'playerName': 'Darkness'
            ,'card': None}
        ],
        'trickNum': 3,
        'trickSuit': 'c',
        'currentTrick': [
            {'playerName': 'Kazuma'
            ,'card': '3c'},
            {'playerName': 'Aqua'
            ,'card': None},
            {'playerName': 'Megumin'
            ,'card': None},
            {'playerName': 'Darkness'
            ,'card': None}
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
    "RequestAction" : False,
    "data" : {
        'trickNum': 3,
        'trickWinner': 'Aqua',
        'cards': ['4c','7c','9c','Tc']
    }
}
```

* RoundEnd
```
{
    "event_name" : "RoundEnd",
    "broadcast" : True,
    "RequestAction" : False,
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
        'trickNum': 3
    }
}
```

* GameOver
```
{
    "event_name" : "GameOver",
    "broadcast" : True,
    "RequestAction" : False,
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
        'trickNum': 7,
        'Winner': 'Kazuma'
    }
}
```

# Reference