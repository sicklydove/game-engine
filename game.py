import sys
import time
import pickle

"""
	Simple engine for text-based adventure games
	Version 0.1 09/12/15
	laurie@farragar.com


	Big TODOs:
		Implement items, stats & transition dependencies
		Does loading drop into the current game state?
		Improve IO - print and raw_input doesn't cut it.
		Improve state key/transition usability
		Option to disable magic 0.2s wait
		Print CMDs
		Pass game state not game object to achievement unlock fns
		DOCUMENTATION
"""

WINDOW_COLS = 100

def format_msg(msg):
	formatted = ''

	for i, char in enumerate(msg):
		if i % WINDOW_COLS == 0:
			formatted += '\n'

		formatted += char

	return formatted

class Achievement:
	def __init__(self, title, msg, should_unlock):
		self.title = title
		self.msg = msg
		self.should_unlock = should_unlock

class State:
	def __init__(self, key, msg, transitions):
		self.key = key
		self.msg = format_msg(msg)
		self.transitions = transitions
		self.transitions_map = {transition.key: transition for transition in transitions}

class Transition:
	def __init__(self, key, msg, state_key):
		self.key = key
		self.msg = msg
		self.state_key = state_key

class Writer:

	@staticmethod
	def print_unlock_msg(achievement):
		unlock_msg = 'Achievement unlocked!'
		padding = max([len(achievement.msg), len(achievement.title), len(unlock_msg)]) * '*'

		lines = [padding, unlock_msg, '', achievement.title, achievement.msg, padding]

		unlock_msg = '\n'.join(lines)

		print(unlock_msg)

	@staticmethod
	def print_state_text(state):
		if state.key == 'MENU':
			print(state.msg)
		else:
			for char in state.msg:
				time.sleep(0.02)
				print(char, end = '', flush = True)

	@staticmethod
	def print_choices(state):
		print ('\n', end = '')
		for transition in state.transitions:
			print('[%s] - %s'%(transition.key, transition.msg))

	@staticmethod
	def print_leaving_msg():
		print('Laters')

	@staticmethod
	def print_game_over():
		print ('Game over!\nPress any key to close')

class Game:

	states_reached = set([])
	unlocked_achievements = set([])
	
	def __init__(self):
		self.over = False

		self.cmds = {
			'X' : self.save_and_quit,
			'Y' : self.quit
		}

		self.load()

		self.states = {state.key: state for state in self.get_states()}
		
		self.current_state = self.states['MENU']
		self.path = [self.current_state]


	def load(self):
		try:
			achievements_file = open('./achievements.sav', 'rb')
			self.unlocked_achievements = pickle.load(achievements_file)
			achievements_file.close()

			nodes_file = open('./nodes.sav', 'rb')
			self.states_reached = pickle.load(nodes_file)
		except FileNotFoundError:
			self.save()
	
	def save(self):
		achievements_file = open('./achievements.sav', 'wb+')
		pickle.dump(self.unlocked_achievements, achievements_file)
		achievements_file.close()

		nodes_file = open('./nodes.sav', 'wb+')
		pickle.dump(self.states_reached, nodes_file)
		nodes_file.close()

	def save_and_quit(self):
		self.save()
		self.quit()

	def test_achievements(self):
		for a in self.achievements:
			if a.should_unlock(self) and a.title not in game.unlocked_achievements:
				self.unlock(a)

	def unlock(self, achievement):
		Writer.print_unlock_msg(achievement)
		self.unlocked_achievements.add(achievement.title)

	def quit(self):
		Writer.print_leaving_msg()
		sys.exit()

	def step(self):
		self.over = not self.current_state.transitions

		Writer.print_state_text(self.current_state)
		Writer.print_choices(self.current_state)

		new_state = None
		while new_state is None and not self.over:
			try:
				choice = input('--> ').upper()
				if choice in self.cmds:
					self.cmds[choice]()

				new_state = self.states[self.current_state.transitions_map[choice].state_key]

				self.current_state = new_state
				self.path.append(self.current_state.key)

				if new_state.key not in self.states_reached:
					self.states_reached.add(new_state.key)

			except KeyError:
				pass
	
	def achievements_msg(self):
		msg = '\n'
		for achievement in self.achievements:

			msg += '[%s] ' % 'X' if achievement.title in self.unlocked_achievements else ''
			msg += achievement.title
			msg += ' - '
			msg += achievement.msg
			msg += '\n'

		return msg
	
	#TODO - states/achievements to be read from file
	#TODO - bit grim; needs wrapping so we execute fns at runtime
	def get_states(self):
		all_states = [

			State(
				key='MENU',
				msg='''
						Title
					''',
               transitions=[ 
					Transition('S', 'Start a new game', 'START'),
					Transition('A','View achievements', 'ACHIEVEMENTS'),
					Transition('E', 'Exit', 'EXIT')
				]
			),

			State(
				key='EXIT',
				msg='',
				transitions=[],
			),

			State(
				key='ACHIEVEMENTS',
				msg=self.achievements_msg(),
				transitions=[
					Transition('M', 'Return to menu', 'MENU')
				]
			),

			State(
				key='START',
				msg='''
					Foo
					''',
				transitions=[],
				),
			]

		return all_states

	achievements = [
		Achievement(
			'Example Achievement Title',
			'Example achievement text',
			lambda game: 'FOO' in game.path
		),
	]

if __name__ == '__main__':
	game = Game()

	while not game.over:
		game.step()
		game.test_achievements()

	Writer.print_game_over()
	input()

	game.save_and_quit()
