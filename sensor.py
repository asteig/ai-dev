"""
filename: sensor.py
author: asteig
license: public domain

The Sensor class listens for the beginning and ending regexes of a particular command and returns the named capture groups from the regexes.
"""
import json
import re
import time

from captures import *
from utils import *

STATUS_QUEUED = 'queued'
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'

# description of WORLDSTATE; initially False
EMPTY_WORLDSTATE = {
	'room': {
		'identifier': None,
		'tz': None,
		'name': None,
		'ty': None,
		'terrain': None,
		'visibility': None,
		'tx': None,
		'kind': None,
		'exits': None
	},
	'list': {
		'items': {
			'id': None,
			'item': None,
			'price': None
		}
	}
}


class Sensor:
	
	# queue all commands waiting for a response
	CAPTURE_QUEUE = []
	CAPTURE_HISTORY = []
	
	# set capture groups
	def __init__(self, captures):
		self.captures = CMD_CAPTURES
		
	"""
	return: data of a completed capture or False
	"""
	def read(self, packet):
		# unpack the packet
		# TODO: handle bad packets
		self.data = json.loads(packet)
		
		# send all commands to the capture queue
		if 'cmd_txt' in self.data:
			return self._queueCapture(self.data['cmd_txt'])
		
		# extract data from MUD response text
		if 'response_txt' in self.data:
			# should we start the capture?
			if self._start():
				# starting capture; no data yet
				return False
			
			# only add response when sensor is actively capturing
			if self.active and self.active['status'] == STATUS_ACTIVE:
				# get most-recent response text from MUD
				sText = self.data['response_txt']
				
				# add response text to capture
				self.active['response'].append(sText)

				# ending capture; return data from captures
				if self._stop(sText):
					return self._getNamedCaptures()
			
		return False
		
	# collapse to WORLDSTATE data
	# UNIVERSAL FORMATTING (should apply to all MUDs)
	# NOTHING MUD-SPECIFIC BELOW THIS LINE!!!!!
	def _filter(self, captured_data):
		# only keep WORLDSTATE properties
		filtered_data = EMPTY_WORLDSTATE.copy()
		for name in captured_data:
			# split into a path list
			state_path = name.split('_')
			
			# get the raw value for this state property
			raw_value = captured_data[name]
			
			# do some gross formatting... :(
			# FORMATS DEFINED HERE:
			# TODO: I'm only handling 2 levels :(
			if state_path[-1] in ['json', 'list']:
				# get format; remove it from state_path
				state_path, frmt = state_path[:-1], state_path[-1]
				
				# decode json strings
				if frmt == 'json':
					frmt_value = json.loads(raw_value)
					# add json data to filtered results
					filtered_data[state_path[0]].update(frmt_value)
				# split 'and' lists from descriptions
				elif frmt == 'list':
					frmt_value = splitTxtList(raw_value)
					filtered_data[state_path[0]][state_path[1]] = frmt_value
			# don't format this at all!!!
			else:
				filtered_data[state_path[0]][state_path[1]] = raw_value
		
		return filtered_data
			
	# TODO: make sure the data isn't being overwritten...
	def _getNamedCaptures(self):
		# get current captures and response text
		captures = self.active['captures']
		response = self.active['response']
		
		# combine all data
		all_captured = {}
		
		# stack items
		items = []
		
		# search each line of the response for named captures
		for line in response:
			for regex in captures:
				if result := re.search(regex, line):
					groups = result.groupdict()
					captured = {k:v for k,v in groups.items() if v is not None}
					# TODO: too specific; should stack any repeated keys
					if 'item' in groups.keys():
						items.append(captured)
					else:
						all_captured.update(captured)
		if items:
			all_captured['items'] = items
			
		# filter raw matches 
		return self._filter(all_captured)

	# add recognized commands to the capture queue
	def _queueCapture(self, cmd_txt):
		# parse command line
		cmd_root = cmd_txt.split(' ')[0]
		cmd_args = cmd_txt.split(' ')[1:]
		
		# expand alias
		for cmd in CMD_ALIASES:
			if cmd_root in CMD_ALIASES[cmd]:
				cmd_root = cmd
		
		# add recognized command to queue
		if cmd_root in self.captures:     
			new_cmd = {
				'action': cmd_root.lower(),
				'args': cmd_args,
				'cmd_root': cmd_root,
				'captures': self.captures[cmd_root],
				'data': {},
				'response': [],
				'status': STATUS_QUEUED,
			}
			
			# add command capture to the queue
			self.CAPTURE_QUEUE.append(new_cmd)
			
			# no data to return yet
			return False
				
		# wtf do you want me to do with this???
		print('I don\'t know that command!', cmd_root)
		False
	
	def _start(self):
		# get active capture
		self.active = self.CAPTURE_QUEUE[0] if self.CAPTURE_QUEUE else False
		
		# only queued captures can be started...
		if self.active and self.active['status'] == STATUS_QUEUED:
			# if the first regex matches current line
			start_regex = self.active['captures'][0]
			if re.search(start_regex, self.data['response_txt']):
				self.active['status'] = STATUS_ACTIVE
				self.active['response'].append(self.data['response_txt'])
				return True

		# probably already started
		return False
	
	def _status(self):
		if self.CAPTURE_QUEUE:
			return self.CAPTURE_QUEUE[0]['status']
		else:
			return False

	def _stop(self, sText):
		# only an active capture can be stopped...
		if self.active['status'] != STATUS_ACTIVE:
			return False
		
		# if the last regex matches the last line of the response...
		if re.search(self.active['captures'][-1], sText):
			self.active['status'] = STATUS_SUCCESS
			self.CAPTURE_HISTORY.append(self.active)
			self.CAPTURE_QUEUE.pop(0)
			return True
			
		# not the end of the capture
		return False