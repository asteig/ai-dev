# standard python libraries
import time
import json

# my includes
from node import *
from utils import *


# TODO: obviously find a home for this with goals...
EXPAND = False

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
		print(percept)
		
		# not room data...
		if 'room' not in percept:
			return False
		
		# get room info
		room = percept['room']
		
		# look for node in graph
		node_id = room['identifier']
		# "I member!"
		if node_id in self.EXPLORED:
			colorNote('EXISTING NODE!!! '+node_id)
			node = self.EXPLORED[node_id]
		else:
		# I need to add this one!
			colorNote('NEW NODE!!! '+node_id)
			parent_id = self.WORLDSTATE['prev_id'] if 'prev_id' in self.WORLDSTATE else False
			room['parent'] = self.EXPLORED[parent_id] if parent_id else False
			room['action'] = percept['action']
			node = Node(room)
		
		# update edges
		parent_id = node.parent_id
		if parent_id and node.action in REVERSE_ACTION:
			# parent to child
			self.EXPLORED[parent_id].edges[node.action] = node.id
			# child to parent
			node.edges[REVERSE_ACTION[node.action]] = parent_id
		
		# came in from a different direction...
		prev_id = self.WORLDSTATE['prev_id'] if 'prev_id' in self.WORLDSTATE else False
		if prev_id and prev_id != parent_id:
			prev_node = self.EXPLORED[prev_id]
			prev_node.edges[percept['action']] = node.id
			node.edges[REVERSE_ACTION[percept['action']]] = prev_id
			# TODO: double check I need this...
			self.EXPLORED[prev_id] = prev_node
		
		self.EXPLORED[node.id] = node
		print('EXPLORED', self.EXPLORED)
		
		# finally, set prev node to current node
		self.WORLDSTATE['prev_id'] = node.id

		return node
			
	def _frontier(self):
		return [n_id for n_id in self.EXPLORED if not self.EXPLORED[n_id].expanded()]
	
	# update internal state, choose next action
	def next(self, percept):
		print(percept)
		# update internal state
		self.percept = percept
		
		if EXPAND:
			# expand the internal map
			node = self._expand(percept)
			
			# what direction now?
			# is the frontier empty?
			frontier = self._frontier()
			
			# nothing left to explore...
			if not frontier:
				return False
			
			# our current room has unexplored exits
			if node.id in frontier:
				# return first unexplored edge...
				for action in node.edges:
					if not node.edges[action]:
						return action
			
			# what about any unexplored nodes up the tree?
			check_node = node
			while check_node:
				if not check_node.expanded():
					for action in check_node.edges:
						if not check_node.edges[action]:
							print('check_node', check_node)
							return action
				# move on to the next node...
				parent_id = check_node.parent_id
				check_node = self.EXPLORED[parent_id] if parent_id else False
					
			# TODO: probably some edge cases to catch... maybe?
			# TODO: record this somewhere if it ever happens......
			print('HEY! What\'s going on?!')
