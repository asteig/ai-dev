from utils import *
from task import * 
from node import *

# TODO: Save room data to database of some kind
class Expand(Task):
	
	# for graph-solving problems
	# collection of nodes
	EXPLORED = {}
	
	WORLDSTATE = {}
	
	# TODO: move to tasks
	def next(self, percept):	
		# not room data...
		if 'room' not in percept:
			return False
		
		# get room info
		room = percept['room']
		
		# look for node in graph
		node_id = room['identifier']

		# "I member!"
		if node_id in self.EXPLORED:
			colorNote('EXISTING NODE!!! '+self.EXPLORED[node_id].name)
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

		# TODO: should I move this logic to a knowledge base?
		if not self._frontier():
			# already expanded; no need to expand any more!
			MODE_EXPAND = False
			
		# finally, set prev node to current node
		self.WORLDSTATE['prev_id'] = node.id

		# what direction now?
		# is the frontier empty?
		frontier = self._frontier()
		
		# nothing left to explore...
		if not frontier:
			colorNote('~*~*~*~*~*~*~*~ALL EXPLORED!!!~*~*~*~*~*~*~*~')
			self._serialize()
			return self.data
		
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
					# climb back up the tree
					if not check_node.edges[action]:
						return REVERSE_ACTION[node.action]
			# move on to the next node...
			parent_id = check_node.parent_id
			check_node = self.EXPLORED[parent_id] if parent_id else False

		return False

	def _frontier(self):
		unexplored = [n_id for n_id in self.EXPLORED if not self.EXPLORED[n_id].expanded()]
		return unexplored
	
	def _serialize(self):
		self.data['map'] = {}
		for node_id in self.EXPLORED:
			self.data['map'][node_id] = self.EXPLORED[node_id].data
			self.data['map'][node_id]['parent'] = self.data['map'][node_id]['parent'].id
			self.data['map'][node_id]['edges'] = self.EXPLORED[node_id].edges
		