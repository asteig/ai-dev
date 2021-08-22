# standard python libraries
from sh import tail

# my stuff
from sensor import Sensor
from agent import Agent

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
	
	def EXECUTE(self, cmd_txt):
		print('WOAH! EXECUTE THIS:', cmd_txt)
	
	def start(self):
		# runs forever 
		while True:
			for packet in tail('-f', '/home/zaya/Apps/MUSHclient/x/sync.in', _iter=True):
				
				# update the agent of any changes to the WORLDSTATE
				if data := self.sensor.read(packet):
					self.agent.update(data)
					
			# repeat forever! :D