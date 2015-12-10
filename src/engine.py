import sys
import pickle

import writer

"""
    Simple engine for text-based adventure games
    Version 0.1 09/12/15
    laurie@farragar.com


    Big TODOs:
        Implement items, stats & transition dependencies
        Improve IO - print and raw_input doesn't cut it.
        Improve state key/transition usability
        Option to disable magic 0.2s wait
        Print CMDs
        Pass game state not game object to achievement unlock fns
        DOCUMENTATION
"""

class Achievement:
    def __init__(self, title, msg, should_unlock):
        self.title = title
        self.msg = msg
        self.should_unlock = should_unlock

class State:
    def __init__(self, key, msg, transitions):
        self.key = key
        self.msg = msg
        self.transitions = transitions

    def init(self, game_state):
        if callable(self.msg):
            self.msg = self.msg(game_state)

        if callable(self.transitions):
            self.transitions = self.transitions(game_state)

        self.transitions_map = {
            transition.key: transition for transition in self.transitions
        }

class Transition:
    def __init__(self, key, msg, state_key):
        self.key = key
        self.msg = msg
        self.state_key = state_key

class Game:
    unlocked_achievements = set([])

    def __init__(self, states, achievements=[]):
        self.over = False

        self.cmds = {
            'X' : self.save_and_quit,
            'Q' : self.quit
        }

        self.states = states
        self.achievements = achievements

        self.states = {
            state.key: state for state in self.states
        }

        
        self.current_state = self.states['MENU']
        self.current_state.init(self)

        self.load()

    def load(self):
        try:
            state_file = open('save/state.sav', 'rb')
            game_state = pickle.load(state_file)
            state_file.close()

            self.unlocked_achievements = game_state['unlocked_achievements']
            self.path = game_state['path']

            self.states['CONTINUE'] = self.states[self.path[-1]]
        except (FileNotFoundError, EOFError):
            self.save()

    def get_game_state(self):
        return {
            'unlocked_achievements': self.unlocked_achievements,
            'path': self.path,
            'stats': None,
            'items': None
        }

    def save(self):
        state_file = open('save/state.sav', 'wb+')
        pickle.dump(self.get_game_state(), state_file)
        state_file.close()

    def save_and_quit(self):
        self.save()
        self.quit()

    def test_achievements(self):
        for a in self.achievements:
            if a.should_unlock(self) and a.title not in game.unlocked_achievements:
                self.unlock(a)

    def unlock(self, achievement):
        writer.print_unlock_msg(achievement)
        self.unlocked_achievements.add(achievement.title)

    def quit(self):
        writer.print_leaving_msg()
        sys.exit()

    def step(self):
        self.over = not self.current_state.transitions

        writer.print_state_text(self.current_state)
        writer.print_choices(self.current_state)

        new_state = None
        while new_state is None and not self.over:
            try:
                choice = input('--> ').upper()
                if choice in self.cmds:
                    self.cmds[choice]()

                new_state = self.states[self.current_state.transitions_map[choice].state_key]
                new_state.init(self)

                self.current_state = new_state
                self.path.append(self.current_state.key)

            except KeyError:
                pass
    