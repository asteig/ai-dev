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

	# current "view" of the agents
	percept = False
	
	def __init__(self, params):
		# TODO: auto-expand params
		#self.name = params['name']
		
		# task-specific logic
		if CURRENT_MISSION:
			print('CURRENT_MISSION:', CURRENT_MISSION)
			self.mission = CURRENT_MISSION
		
		# what does the agent want?
		self.goals = params['goals'] if 'goals' in params else False
		
		# TODO: have agent meander towards goals
		# handle existential crises
		# if not goals:
		# 	colorNote('ERROR: You don\'t know what you want! Try again.')
		# 	colorNote('It\'s okay! We\'ll just explore! :)')
	
	# get all actions available to the current (or passed) state
	def _actions(self, state=False):
		return

	# update internal state, choose next action
	def next(self, percept):
		print('YO!!!')
		print('AGENT NEXT_______ _______ _______')
		# update internal state
		self.percept = percept
		
		# TODO: should be "task"
		# should we be expanding the map?
		if self.mission:
			print('here')
			# expand the internal map
			next_action = self.mission.next(percept)
			return next_action
