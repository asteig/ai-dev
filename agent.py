# standard python libraries
import time
import json

# my includes
from node import *
from utils import *


class Agent:
	
	# for graph-solving problems
	# collection of nodes
	EXPLORED = {}
	
	# all percepts combined into a single worldstate
	WORLDSTATE = {}

	# current "view" of the agents
	percept = False
	
	def __init__(self, params):
		# TODO: auto-expand params
		#self.name = params['name']
		
		# what does the agent want?
		goals = params['goals'] if 'goals' in params else False
		
		# TODO: have agent meander towards goals
		# handle existential crises
		if not goals:
			colorNote('ERROR: You don\'t know what you want! Try again.')
			colorNote('It\'s okay! We\'ll just explore! :)')
	
	# get all actions
	# without state, returns ALL actions in the environment
	# with a state supplied, it returns ALL actions available at that moment.
	def _actions(self, state=False):
		return
		
	def _expand(self, percept):
	
		print('expand:')
		if self.EXPLORED['expanded']:
			return True
		
		# look for node in graph
		node_id = percept['identifier']
		# "I member!"
		if node_id in self.EXPLORED:
			colorNote('EXISTING NODE!!! '+node_id)
			node = self.EXPLORED[node_id]
		else:
		# I need to add this one!
			colorNote('NEW NODE!!! '+node_id)
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
		
		# in case a second parent emerges
		prev_id = self.WORLDSTATE['prev_id']
		if prev_id != parent_id:
			prev_node = self.EXPLORED[prev_id]
			prev_node.edges[percept['action']] = node.id
			node.edges[REVERSE_ACTION[percept['action']]] = prev_id
			# TODO: double check I need this...
			self.EXPLORED[prev_id] = prev_node
		
		self.EXPLORED[node.id] = node
		
		# is the map expanded?
		self.EXPLORED['expanded'] = [self.EXPLORED[n_id].expanded() for n_id in self.EXPLORED]
		
		# finally, set prev node to current node
		self.WORLDSTATE['prev_id'] = node.id

		return node
	
	# update agent's internal state
	# DEV: return a node if percept describes a room
	def update(self, percept):
		
		# update internal state
		print('update the worldstate:', percept)

		# TODO: fucking messssyyy ew 
		# NORMALILZE DATA (everything but rooms should have the correct structure
		if 'identifier' in percept:
			percept = {
				'room': percept
			}
			
		# ew, more of this crap. :(
		if 'wearing' in percept:
			percept = {
				'inventory': percept
			}
		
		# update WORLDSTATE
		self.WORLDSTATE.update(percept)
	
	# update internal state, choose next action
	def next(self, percept):
		# update internal state
		self.WORLDSTATE = self._update(percept)
