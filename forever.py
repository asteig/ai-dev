# python packages
from sh import tail
import json

# my includes
from utils import *
from captures import *
from agent import Agent


# queue of commands waiting to run...
CMDS = []
HISTORY = []

# all commands with captures are valid
VALID_CMDS = list(CMD_CAPTURES.keys())

# goals
GOAL_EXPAND = 'expand'


class Environment: 

	def __init__(self, params):
		self.player = params['agent']
		
	# handle input from the player
	def handleCommandSent(self, packet):
		cmd_txt = packet['cmd_txt']
		
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
			CMDS.append(new_cmd)

	def handleTxtReceived(self, packet):

		# get line text
		sText = packet['txt']
		
		# return False if there's no commands in the queue
		if not CMDS:
			return False

		next_cmd = CMDS[0]
		# print('HERE', next_cmd)
		
		# command doesn't work...
		if re.search(REGEX_FAILED, sText):
			next_cmd['status'] = STATUS_FAILED
			next_cmd['completed'] = packet['received']
			HISTORY.append(next_cmd)
			CMDS.pop(0)
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
			CMDS.pop(0)
			
			# update the agent
			next_action = player.update(captured)
	
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
	player = Agent({'name': 'Zaya', 'goal': GOAL_EXPAND})
	
	# place agent in environment
	game = Environment({'agent':player})
	
	# let's go!!
	game.start()

