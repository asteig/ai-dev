# python packages
from sh import tail
import json

# my includes
from utils import *
from captures import *
from agent import Agent


# queue of commands waiting to run...
CMD_QUEUE = []
CMD_HISTORY = []

### GOAL CHECKS
# TODO: decide where to actually put this...
# represent each goal as its desired end state.

# search graph for unexpanded nodes
def is_expanded(graph):
	for node in self.GRAPH:
		for edge in node.edges:
			if not edge:
				return False
	return True
### END GOAL CHECKS

### MAGIC COMMANDS
MAP_START = False
MAP_HISTORY = []
# just for development...
def _mapStart(graph):
	print('_mapStart')
	MAP_START = True
	return graph
	
def _mapShow(graph):
	print('_mapShow')
	# make [y][x] grid with a width of 13
	display_grid = []
	for y in range(0, 13):
		row = [' '] * 13
		display_grid.append(row)

	for node_id in graph:
		node = graph[node_id]
		print(node_id, node.x, node.y)
		display_grid[node.y][node.x] = '#'
		
	for row in display_grid:
			print(''.join(row))
	
	print('fuck')

def _mapStop(graph):
	print('_mapStop')
	MAP_START = False
	return graph
	
def _mapReset(graph):
	print('_mapReset')
	return []
	
def _mapPrint(graph):
	flat_graph = []
	for node_id in graph:
		node = graph[node_id]
		flat_graph.append({
			'id': node.id,
			'parent_id': node.parent_id,
			'action': node.action,
			'path_cost': node.path_cost,
			'edges': node.edges
		})
	print('---graph data structure:')
	print(flat_graph)
	print('---')
	return graph
### END MAGIC COMMANDS

# TODO: make dynamic...
MAGIC_PHRASES = {
	'You exclaim: START!!': _mapStart,
	'You exclaim: SHOW!!': _mapShow,
	'You exclaim: STOP!!': _mapStop,
	'You exclaim: RESET!!': _mapReset,
	'You exclaim: PRINT!!': _mapPrint
}

class Environment: 

	def __init__(self, params):
		self.player = params['agent']
		
	# handle input from the player
	def handleCommandSent(self, packet):
		
		cmd_txt = packet['cmd_txt']
		print('COMMAND TEXT:', cmd_txt)
		# add recognized commands to the queue
		if cmd_txt in CMD_CAPTURES:
			new_cmd = {
				'action': cmd_txt,
				'received': packet['received'],
				'status': STATUS_QUEUED,
				'captures': CMD_CAPTURES[cmd_txt],
				'response': [],
				'captured': {},
				'completed': False
			}
			CMD_QUEUE.append(new_cmd)
			
			if MAP_START:
				MAP_HISTORY.append(cmd_txt)

	def handleTxtReceived(self, packet):

		# get line text
		sText = packet['txt']
		
		### dev
		# is this a magic command?
		if sText in MAGIC_PHRASES:
			magic_fn = MAGIC_PHRASES[sText]
			colorNote('MAGIC!!!!!! ')
			player.graph = magic_fn(player.EXPLORED)
			return True
		### /dev
		
		# return False if there's no commands in the queue
		if not CMD_QUEUE:
			return False

		next_cmd = CMD_QUEUE[0]
		
		# command doesn't work...
		if re.search(REGEX_FAILED, sText):
			next_cmd['status'] = STATUS_FAILED
			next_cmd['completed'] = packet['received']
			CMD_HISTORY.append(next_cmd)
			CMD_QUEUE.pop(0)
			return False
		
		start_capture = next_cmd['captures'][0]
		stop_capture = next_cmd['captures'][-1]

		# start capture
		if re.search(start_capture, sText):
			next_cmd['status'] = STATUS_ACTIVE
		
		if next_cmd['status'] == STATUS_ACTIVE:
			# add this line to the response
			next_cmd['response'].append(sText)
		
		# stop capture
		if re.search(stop_capture, sText):
			captured = getCaptured(next_cmd['captures'], next_cmd['response'])
			captured['action'] = next_cmd['action']
			CMD_QUEUE.pop(0)
			
			# update the agent
			print('update the agent...')
			next_action = player.update(captured)
	
	
## JUST FOCUS ON MAKING A MAP!!!!
	
	def start(self):
		# TODO: basic stats
		print('PLAYER:', self.player.name)
		print('SESSION START:')
		print('\n\n\n')
		
		# runs forever, reading output from the MUD line by line...
		while True:

			for packet in tail('-f', '/home/zaya/Apps/MUSHclient/x/sync.in', _iter=True):

				data = json.loads(packet)
				
				if 'cmd_txt' in data:
					self.handleCommandSent(data)
					
				if 'txt' in data:
					self.handleTxtReceived(data)
			
if __name__ == "__main__":
	
	# init a player agent
	player = Agent({
		'name': 'Zaya', 
		'goal': is_expanded
	})
	
	# place agent in environment
	game = Environment({'agent':player})
	
	# let's go!!
	game.start()

