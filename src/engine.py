import copy
import sys
import pickle

import writer
from player import Player

"""
    Simple engine for text-based adventure games
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
    def __init__(self, key, msg, transitions, entry_hook=lambda x: None):
        self.key = key
        self.msg = msg
        self.transitions = transitions
        self.entry_hook = entry_hook

    def init(self, game_state):
        if callable(self.msg):
            self.msg = self.msg(game_state)

        if callable(self.transitions):
            self.transitions = self.transitions(game_state)

        self.transitions_map = {
            transition.key: transition
                for transition in self.transitions
                    if transition.is_active(game_state)
        }

class Transition:
    def __init__(self, key, msg, target_state_key, is_active=lambda x: True):
        self.key = key
        self.msg = msg
        self.target_state_key = target_state_key
        self.is_active = is_active

class Game:
    unlocked_achievements = set([])

    def __init__(self, states, achievements=[]):
        self.cmds = {
            'X' : self.save_and_quit,
            'Q' : self.quit
        }

        self.states = states
        self.achievements = achievements

        self.game_state = {
            'path': self.path,
            'stats': self.player.stats,
            'items': self.player.items
        }

        self.states = {
            state.key: state for state in self.states
        }

        self.has_save = self.load_persistent()

        self.reset_state()

    @property
    def current_state(self):
        return self.states[self.path[-1]]

    def load_persistent(self):
        try:
            state_file = open('save/state.sav', 'rb')
            game_state = pickle.load(state_file)
            state_file.close()

            self.unlocked_achievements = game_state['unlocked_achievements']

            self.states['CONTINUE'] = self.states[game_state['path'][-1]]
            self.states['CONTINUE'].entry_hook = lambda game: game.load_game()
        except (FileNotFoundError, EOFError):
            return False

        return True

    def load_game(self):
        state_file = open('save/state.sav', 'rb')
        game_state = pickle.load(state_file)
        state_file.close()

        self.path = game_state['path']
        self.stats = game_state['stats']
        self.items = game_state['items']

        # Unbind the entry hook incase we ever loop back to this state
        self.states['CONTINUE'].entry_hook = lambda x: None

    def get_game_state(self):
        return {
            'unlocked_achievements': self.unlocked_achievements,
            'path': self.path,
            'stats': None,
            'items': None
        }

    def reset_state(self):
        self.over = False
        self.path = ['MENU']
        self.current_state.init(self)
        self.player = Player('TODO')

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
        sys.exit()

    def step(self):
        self.over = not self.current_state.transitions

        writer.print_state_text(self.current_state)

        choices = [x for x in self.current_state.transitions
            if x.is_active(self)
        ]

        writer.print_choices(choices)

        new_state = None
        while new_state is None and not self.over:
            try:
                choice = input('--> ').upper()
                if choice in self.cmds:
                    self.cmds[choice]()

                new_state = self.states[self.current_state.transitions_map[choice].target_state_key]
                new_state.init(self)

                self.path.append(new_state.key)

            except KeyError:
                pass
    