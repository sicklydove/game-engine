from engine import State, Achievement, Transition

states = [
    State(
       key = 'MENU',
       msg = "Title",
       transitions = [ 
            Transition('S', "Start a new game", 'START'),
            Transition('A', "View achievements", 'ACHIEVEMENTS'),
            Transition('E', "Exit", 'EXIT')
        ]
    ),

    State(
        key = 'EXIT',
        msg = "",
        transitions = [],
    ),

    State(
        key = 'ACHIEVEMENTS',
        msg = 'TODO: self.achievement_msg()',
        transitions = [
            Transition('M', 'Return to menu', 'MENU')
        ]
    ),

    State(
        key = 'START',
        msg = 'FOO',
        transitions = [],
    ),
]

achievements = [
    Achievement(
        "Example Achievement Title",
        "Example achievement text",
        lambda game: 'FOO' in game.path
    ),
]
