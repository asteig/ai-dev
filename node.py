from utils import *

class Node:

	def __init__(self, state):

		self.id = state['identifier']
		self.parent_id = state['parent_id']
		self.action = state['action']
		#self.path_cost ... TODO
		self.edges = {}
		
		# init all edges as unexplored
		available_actions = self._splitExits(state['exits'])
		for a in available_actions:
			self.edges[a] = False
				
		"""
		# not sure what we've seen; queue all exits for expansion
		for exit in exits:
			action = direction_alias[exit]
			# only known directional commands (no 'enter door', etc.)
			if action in CMD_CAPTURES:
				self.edges[action] = False
		
		# update parent!
		if parent_id:
			action = node['action']
			
			# update the parent
			parent_node = self.EXPLORED[parent_id]
			parent_node['edges'][action] = room_id
			print('did it update parent?', self.EXPLORED[parent_id])
			
			# we know what what action goes back to the parent
			node['edges'][reverse_action[action]] = parent_id
		"""
		
	def _splitExits(self, exits):
		txt = exits.replace(' and ', ', ')
		exits = txt.split(', ')
		return exits