import time

COLS = 100

def init(self, cols=COLS):
    global COLS
    COLS = cols
       
def format(msg):
    formatted = ''

    for i, char in enumerate(msg):
        if i % COLS == 0:
            formatted += '\n'

        formatted += char

    return formatted

def print_unlock_msg(achievement):
    unlock_msg = 'Achievement unlocked!'

    msg = self.format(achievement.msg)

    padding = min(
        max([
                len(msg),
                len(achievement.title),
                len(unlock_msg)
           ]),
        COLS
    ) * '*'

    lines = [padding, unlock_msg, '', achievement.title, msg, padding]

    unlock_msg = '\n'.join(lines)

    print(unlock_msg)

def print_state_text(state):
    if state.key == 'MENU':
        print(format(state.msg))
    else:
        for char in format(state.msg):
            time.sleep(0.02)
            print(char, end = '', flush = True)

def print_choices(state):
    print ('\n', end = '')
    for transition in state.transitions:
        print(format('[%s] - %s'%(transition.key, transition.msg)))

def print_leaving_msg():
    print('Laters')

def print_game_over():
    print ('Game over!\nPress any key to close')