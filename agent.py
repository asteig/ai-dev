# my includes
from node import *
from utils import *
import time
import json

MSG_FILE = 'data/messages.json'

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

	# current "view" of the agent
	percept = False
	
	def __init__(self, params):
		# TODO: auto-expand params
		self.name = params['name']
		self.goal = params['goal']
		
		self.message('my first test message! :)')
	
	# get all actions
	# without state, returns ALL actions in the environment
	# with a state supplied, it returns ALL actions available at that moment.
	def getAllActions(self, state=False):
		pass
	
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
			next_action = self.next(node)
			print('GO:', next_action)
			#return self.next(next_action)
	
	# choose next action from internal state
	def next(self, node):
		# are there any unexplored nodes at all?
		if self.checkGoal():
			print('You got it already, champ! Good job!')
			return False
		
		# return first unexplored edge of current node
		if not node.expanded():
			for a in node.edges:
				if not node.edges[a]:
					return a
			
		# what about any unexplored nodes up the tree?
		check_node = node
		while check_node:
			if not check_node.expanded():
				for a in check_node.edges:
					if not check_node.edges[a]:
						# return the reverse of the most recent action
						return REVERSE_ACTION[node.action]
			# move on to the next node...
			parent_id = check_node.parent_id
			check_node = self.EXPLORED[parent_id] if parent_id else False
				
		# uh oh! No unexplored nodes up the tree... what next???
		print('Didn\'t find an unexplored node in the tree. :(')
		
		unexplored = self.getUnexpanded()
		print('unexplored nodes:', unexplored)
	
	# leave a message for the environment...
	def message(self, msg_txt):
		msg = {
			'msg_txt': msg_txt,
			'sent': int(time.time()),
		}
		
		# write to log
		f = open(MSG_FILE, 'a')
		f.write(json.dumps(msg))
		f.close()
		
		return True

	def getUnexpanded(self, graph=False):
		graph = graph if graph else self.EXPLORED
		unexplored = [graph[n_id] for n_id in graph if not graph[n_id].expanded()]
		return unexplored
	
	# add / update a node in EXPLORED, as well as the associated neighbors.
	def expand(self, percept):
		print('percept:', percept)
		# TODO: probably move to update...
		# goal check
		# are all nodes expanded?
		if self.checkGoal():
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
		
		# if an existing node already has a parent_id...
		prev_id = self.WORLDSTATE['prev_id']
		if prev_id != parent_id:
			prev_node = self.EXPLORED[prev_id]
			prev_node.edges[percept['action']] = node.id
			node.edges[REVERSE_ACTION[percept['action']]] = prev_id
			# TODO: double check I need this...
			self.EXPLORED[prev_id] = prev_node
		
		print('EXPANDED:', node.expanded())
		[print(a, ':', node.edges[a]) for a in node.edges]
		print('')
		print('')
		print('')
		
		self.EXPLORED[node.id] = node
		
		# finally, set prev node to current node
		self.WORLDSTATE['prev_id'] = node.id

		return node
		
	# check every node for hanging edges
	def checkGoal(self):
		if self.EXPLORED:
			expanded = [self.EXPLORED[n_id].expanded() for n_id in self.EXPLORED]
			if all(expanded):
				colorNote('~*~*~*~*~*~*~*~*~*~*~*~*\n!!!!!!!EXPANDED!!!!!!!!!\n~*~*~*~*~*~*~*~*~*~*~*~*')
				return True
		return False