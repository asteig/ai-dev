# python packages
from sh import tail
import json
import time

# my includes
from utils import *
from captures import *
from agent import Agent


# queue of commands waiting for captures
CMD_QUEUE = []
CMD_HISTORY = []

CMD_FILE = 'data/cmd_queue.json'

WORLDSTATE = {}

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
	
	if not graph:
		return False
	
	# TODO: less sloppy bounding...
	# make sure the grid is big enough...
	offset_x = abs(min([graph[n_id].x for n_id in graph])) + 5
	offset_y = abs(min([graph[n_id].y for n_id in graph])) + 5
	
	# make [y][x] grid with a width of 13
	display_grid = []
	for y in range(0, (20)):
		row = [' '] * (20)
		display_grid.append(row)

	for node_id in graph:
		node = graph[node_id]
		display_grid[node.y+offset_y][node.x+offset_y] = '#'
		
	for row in display_grid:
			print(''.join(row))

def _mapStop(graph):
	print('_mapStop')
	MAP_START = False
	return graph
	
def _mapReset(graph):
	print('_mapReset')
	return []
	
# print data out using aima data representations... 
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
	
def _mapSave(graph):
	print('Save JSON data:')
	print(json.dumps(graph))
	print('--------------')

####### next
# recommend next action...
# (next unexplored action, closest to current position)
def _mapNext(graph):
	print('_mapNext')
	print(WORLDSTATE)

	
# TODO: make dynamic...
MAGIC_PHRASES = {
	'You exclaim: START!!': _mapStart,
	'You exclaim: SHOW!!': _mapShow,
	'You exclaim: STOP!!': _mapStop,
	'You exclaim: RESET!!': _mapReset,
	'You exclaim: PRINT!!': _mapPrint,
	'You exclaim: SAVE!!': _mapSave,
	'You exclaim: NEXT!!': _mapNext
}
	
	
### END MAGIC COMMANDS

class Environment: 

	def __init__(self, params):
		self.player = params['agent']
		
	def _queueCmdCaptures(self, cmd):
		
		# add recognized commands to the capture queue
		if cmd in CMD_CAPTURES:
			new_cmd = {
				'action': cmd,
				'received': int(time.time()),
				'status': STATUS_QUEUED,
				'captures': CMD_CAPTURES[cmd],
				'response': [],
				'captured': {},
				'completed': False
			}
			
			CMD_QUEUE.append(new_cmd)

	def _getCaptured(self, sText):
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
			return captured
			
		return False
		
		
	# handle input from the player
	def handleCommandSent(self, packet):
		
		cmd_txt = packet['cmd_txt']

		# TODO: handle multiple commands sent at once...
		# TODO: separate queue command function...
		cmd_list = cmd_txt.split('\n')
		
		for cmd in cmd_list:
			self._queueCmdCaptures(cmd)

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

		# "look" for a completed capture group
		# TODO: not sure if the environment should be handling this...
		update = self._getCaptured(sText)
		
		if update:
			# update the worldstate
			print('update the WORLDSTATE...')
			if 'exits' in update:
				WORLDSTATE.update({'room': update})
			
			if 'burden' in update:
				WORLDSTATE.update({'i': update})
			
			# update the player
			self.player.update(update)
	
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

