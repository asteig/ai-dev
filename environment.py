# standard python libraries
import json
from sh import tail
import time
from uuid import uuid4

# my stuff
from agent import Agent
from sensor import Sensor
from utils import *

# the file MUSHcleint checks for new commands
REMOTE_COMMANDS_SRC = '/home/zaya/Apps/MUSHclient/x/remote_commands.json'

# global action sequence...
# mainly used for merging command queues...
ACTION_QUEUE = []

class Environment: 

	def __init__(self, params):
		# set initial WORLDSTATE
		#self.worldstate = params['worldstate']
		
		# create a new agent 
		self.agent = Agent(params['agent'])
		
		# create a new sensor for this world
		self.sensor = Sensor({
			#'captures': params['captures'],
		})
	
	# use the sensor data to update the WORLDSTATE
	def _update(self, data):
		print('data:', data)
	
	# WARNING: this will ACTUALLY SEND a command to the MUD!!!!
	# (make sure you're not calling this infinitely, etc...)
	# TODO: handle that ^^^^
	def EXECUTE(self, cmd_txt):
		print('should execute, eh?')

		# send command to client...
		new_cmd = {
			'cmd_txt': cmd_txt,
			'sent': UTC_UNIX_EPOCH()
		}
		
		# write to remote command file
		file = open(REMOTE_COMMANDS_SRC, 'a')
		file.write(json.dumps(new_cmd)+'\n')
		file.close()
	
	def start(self):
		# clear message log
		file = open(REMOTE_COMMANDS_SRC, 'w')
		file.write('')
		file.close()
		
		# runs forever 
		while True:
			for packet in tail('-f', '/home/zaya/Apps/MUSHclient/x/sync.in', _iter=True):
				# update the agent of any changes to the WORLDSTATE
				if data := self.sensor.read(packet):
					# ask agent wtf to do next...
					if next_action := self.agent.next(data):
						print('EXECUTE:', next_action)
						self.EXECUTE(next_action)
					else:
						colorNote('no next action :)')
			# repeat forever! :D
			
		
