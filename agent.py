# my includes
from node import *
from utils import *

class Agent:
	
	# combine all the captured data into a global state
	WORLDSTATE = {
		'room': {},
		'inventory': {},
		'parent_id': False
	}
	
	# for graph-solving problems
	# collection of nodes
	EXPLORED = {}
	
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
			self.remember(node)
			# choose next action
			return self.next(node)
	
	# choose next action from internal state
	def next(self, node):
		colorNote('What should I do with you?')
		print(node)
	
	# add room to map
	def expand(self, room):
		
		# get previous state
		state = self.WORLDSTATE
		
		# current room id
		room_id = room['identifier']
		
		# add parent_id
		room['parent_id'] = state['parent_id']

		# we haven't seen this room before!
		if room_id not in self.EXPLORED:
			# make a graph node
			node = Node(room)
		else:
			# retreive existing node
			node = self.EXPLORED[room_id]
		
		# set parent_id for next node
		state['parent_id'] = node.id
		
		return node

	# TODO: this is only for graph nodes, what about other data?
	def remember(self, node):
		# add to memory!
		print('saving to memory!')
		print('ID:', node.id)
		print('parent_id:', node.parent_id)
		
		# update parent's edge
		if node.parent_id:
			parent_node = self.EXPLORED[node.parent_id]
			parent_node.edges[node.action] = node.id
			# path back to parent too
			node.edges[reverse_action[node.action]] = parent_node.id
			
		self.EXPLORED[node.id] = node
		print('Saved Nodes:', len(self.EXPLORED))

		
		return self.WORLDSTATE
		
	# check every node for hanging edges
	def checkGoal(self, state):
		for node in self.EXPLORED:
			for edge in node.edges:
				if not edge:
					return False
		return True