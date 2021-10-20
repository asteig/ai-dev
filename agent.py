# standard python libraries
import time
import json
import secrets

# TODO: shouldn't be hardcoded in Agent...
# mission to complete
from missions.expand import *

# TODO: obviously find a home for this with goals...
# lazy "modes"!

# possible statuses for a command... 
STATUS_QUEUED = 'queued'
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'

CURRENT_MISSION = Expand()

class Agent:
	
	# all percepts combined into a single worldstate
	WORLDSTATE = {}

	# action history (resets every run)
	sequence = []
	
	# current position in action sequence (above)
	pos = 0

	# current "view" of the agents
	percept = False
	
	def __init__(self, params):
		# TODO: auto-expand params
		#self.name = params['name']
		
		# task-specific logic
		if CURRENT_MISSION:
			print('CURRENT_MISSION:', CURRENT_MISSION)
			self.mission = CURRENT_MISSION
		
		# TODO: have agent meander towards goals
		# handle existential crises
		# if not goals:
		# 	colorNote('ERROR: You don\'t know what you want! Try again.')
		# 	colorNote('It\'s okay! We\'ll just explore! :)')
	
	# get all actions available to the current (or passed) state
	def _actions(self, state=False):
		return

	# TODO: goal function???

	# update internal state, choose next action
	def next(self, percept):
		print('YO!!!')
		print('AGENT NEXT_______ _______ _______')
		# update internal state
		self.percept = percept
		
		# TODO: handle no missions....
		if self.mission:
			next_action = self.mission.next(percept)
			# add next action to internal history
			self.sequence.append(next_action)
			print('sequence:', self.sequence)
			return next_action

