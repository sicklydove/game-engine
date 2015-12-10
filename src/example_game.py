from engine import State, Achievement, Transition

def achievements_msg(state):
    msg = '\n'

    for achievement in state.achievements:
        msg += '[%s] ' % 'X' if achievement.title in state.unlocked_achievements else ''
        msg += achievement.title
        msg += ' - '
        msg += achievement.msg
        msg += '\n'

    return msg

states = [
    State(
       key = 'MENU',
       msg = "Title",
       transitions = [ 
            Transition('S', "Start a new game", 'START'),
            Transition('C', "Continue saved game", 'CONTINUE'),
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
        msg = achievements_msg,
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
