# my includes
from node import *
from utils import *


class Agent:
	
	# combine all the captured data into a global state
	WORLDSTATE = {
		'room': {},
		'inventory': {}
	}
	
	EXPLORED = {}
	FRONTIER = {}
	
	def __init__(self, params):
		# TODO: auto-expand params
		self.name = params['name']
		self.goal = params['goal']
	
	# update agent's internal state
	def update(self, state):
		colorNote('********* update agent!')
		
		# it's a room!
		# TODO: this should be called by a goal somehow...
		if 'exits' in state:
			# get a graph node
			node = self.expand(state)
			# remember info
			state = self.remember(node)
			# choose next action
			return self.next(state)
	
	# choose next action from internal state
	def next(self, node):
		colorNote('What should I do with you?')
		print(node)
	
	# add room to map
	def expand(self, room):
		
		# get previous state
		state = self.WORLDSTATE
		
		room_id = room['identifier']
		parent_id = state['room']['identifier'] if self.WORLDSTATE['room'] else False
		
		# self; use previous parent
		if room_id == parent_id:
			parent_id = state['room']['parent_id']

		# we haven't seen this room before!
		if room_id not in self.EXPLORED:
			# make a graph node
			node = Node(room)
		else:
			# retreive existing node
			node = self.EXPLORED[room_id]
			
		return node

	# TODO: this is only for graph nodes, what about other data?
	def remember(self, node):
		# add to memory!
		print('saving to memory!', node.id)
		self.EXPLORED[node.id] = node
		print('Saved Nodes:', len(self.EXPLORED))
		return self.WORLDSTATE