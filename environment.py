from sh import tail
import json
import time

# my stuff
from magic import *
from utils import *
from captures import *

class Environment: 

	CAPTURE_QUEUE = []
	CAPTURE_RESULT = []
	
	WORLDSTATE = {
		'prev_id': False
	}

	def __init__(self, params):
		self.player = params['agent']
	
	# add command to end of CAPTURE_QUEUE
	def _queueCmdCaptures(self, cmd_txt):
		
		# add recognized commands to the capture queue
		if cmd_txt in CMD_CAPTURES:
			new_cmd = {
				'action': cmd_txt,
				'received': int(time.time()),
				'status': STATUS_QUEUED,
				'captures': CMD_CAPTURES[cmd_txt],
				'response': [],
				'captured': {},
				'completed': False
			}
			self.CAPTURE_QUEUE.append(new_cmd)

	def _getUpdate(self, sText):
		
		capture_cmd = self.CAPTURE_QUEUE[0]

		# command doesn't work...
		if re.search(REGEX_FAILED, sText):
			# log failed command
			capture_cmd['status'] = STATUS_FAILED
			capture_cmd['completed'] = int(time.time())
			self.CAPTURE_RESULT.append(capture_cmd)
			
			# remove from queue
			self.CAPTURE_QUEUE.pop(0)
			return False
		
		start_capture = capture_cmd['captures'][0]
		stop_capture = capture_cmd['captures'][-1]
		
		# start capture
		if re.search(start_capture, sText):
			capture_cmd['status'] = STATUS_ACTIVE
		
		if capture_cmd['status'] == STATUS_ACTIVE:
			# add this line to the response
			capture_cmd['response'].append(sText)
		
		# stop capture
		if re.search(stop_capture, sText):
			# log capture
			captured = getCaptured(capture_cmd['captures'], capture_cmd['response'])
			capture_cmd['response'] = captured
			captured['action'] = capture_cmd['action']
			self.CAPTURE_RESULT.append(capture_cmd)
			
			# remove from queue
			self.CAPTURE_QUEUE.pop(0)
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
		sText = packet['response_txt']

		### dev
		# is this a magic command?
		if sText in MAGIC_PHRASES:
			magic_fn = MAGIC_PHRASES[sText]
			colorNote('MAGIC!!!!!!         ')
			player.graph = magic_fn(player.EXPLORED)
			return True
		### /dev
		
		# return False if there's no commands in the queue
		if not self.CAPTURE_QUEUE:
			return False

		# "look" for a completed capture group
		update = self._getUpdate(sText)

		# TODO: does the environment need to keep the WORLDSTATE?
		if update:
			print(update)
			# update the worldstate
			if 'exits' in update:
				update['prev_id'] = self.WORLDSTATE['prev_id']
				self.WORLDSTATE.update({'room': update})
			
			if 'burden' in update:
				self.WORLDSTATE.update({'i': update})
			
			# update the player
			next_action = self.player.update(update)
	
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
					
				if 'response_txt' in data:
					self.handleTxtReceived(data)