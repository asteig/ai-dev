# my includes
from node import *
from utils import *

class Agent:
	
	# combine all the captured data into a global state
	WORLDSTATE = {
		'room': {},
		'inventory': {},
		'prev_id': False
	}
	
	# for graph-solving problems
	# collection of nodes
	EXPLORED = {}
	
	def __init__(self, params):
		# TODO: auto-expand params
		self.name = params['name']
		self.goal = params['goal']
	
	# update agent's internal state
	def update(self, percept):
		# it's a room!
		# TODO: this should be called by a goal somehow...
		if 'exits' in percept:
			# get a graph node
			node = self.expand(percept)
			# remember info
			# self.remember(node)
			# choose next action
			return self.next(node)
	
	# choose next action from internal state
	def next(self, node):
		pass
	
	# add room to map
	def expand(self, percept):
		print('expanding...')
		node_id = percept['identifier']
		
		# "I member!"
		if node_id in self.EXPLORED:
			print('EXISTING NODE!!!')
			node = self.EXPLORED[node_id]
			[print(a, ':', node.edges[a]) for a in node.edges]
			print('')
			print('')
			print('')
		else:
		# I need to add this one!
			colorNote('NEW NODE!!!')
			parent_id = self.WORLDSTATE['prev_id']
			percept['parent'] = self.EXPLORED[parent_id] if parent_id else False
			node = Node(percept)
		
		# update edges
		parent_id = node.parent_id
		if parent_id:
			# parent to child
			self.EXPLORED[parent_id].edges[node.action] = node.id
			# child to parent
			node.edges[REVERSE_ACTION[node.action]] = parent_id
		
		# what about if a "2nd" parent?
		prev_id = self.WORLDSTATE['prev_id']
		if prev_id != parent_id:
			prev_node = self.EXPLORED[prev_id]
			prev_node.edges[percept['action']] = node.id
			node.edges[REVERSE_ACTION[percept['action']]] = prev_id
			# TODO: double check I need this...
			self.EXPLORED[prev_id] = prev_node
		
		# what's left to explore?
		print('all_actions:')
		[print(a.upper(), ':', node.edges[a]) for a in node.edges]
		
		self.EXPLORED[node.id] = node
		
		# finally, set prev node to current node
		self.WORLDSTATE['prev_id'] = node.id

		return node

	# TODO: this is only for graph nodes, what about other data?
	def remember(self, node):
		# add to memory!
		print('saving to memory!')
		print('ID:', node.id)
		print('COORDS:', node.x, node.y)
		
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