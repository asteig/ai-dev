from utils import *
from mission import * 
from node import *

# TODO: Save room data to database of some kind
class Expand(Mission):
	
	# for graph-solving problems
	# collection of nodes
	EXPLORED = {}
	
	status = STATUS_QUEUED
	prev_id = False
	
	# TODO: move to tasks
	def next(self, percept):
		# goal check!
		if self.status == STATUS_SUCCESS:
			# nothing left to explore...
			colorNote('~*~*~*~*~*~*~*~ALL EXPLORED!!!~*~*~*~*~*~*~*~')
			self._serialize()
			return self.data
		
		# make sure mission is active (since 'next' is running...)
		self.status = STATUS_ACTIVE
		
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
			parent_id = self.prev_id
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
		if self.prev_id and self.prev_id != parent_id:
			prev_node = self.EXPLORED[self.prev_id]
			prev_node.edges[percept['action']] = node.id
			node.edges[REVERSE_ACTION[percept['action']]] = self.prev_id
			# TODO: double check I need this...
			self.EXPLORED[self.prev_id] = prev_node
		
		self.EXPLORED[node.id] = node

		# MISSION COMPLETE!
		if not self._frontier():
			self.status = STATUS_SUCCESS
			
		# finally, set prev node to current node
		self.prev_id = node.id

		# what action next?
		return self._utility(node)
	
	# TODO: shortest path
	def _utility(self, node):
		
		# our current room has unexplored exits
		if node.id in self._frontier():
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
		print('DATA FROM SERIALIZING:')
		print(self.data)
		