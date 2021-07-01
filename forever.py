from sh import tail
import json
import re 
import utils 
import random

STATUS_QUEUED = "queued"
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'
STATUS_COMPLETE = 'complete'

print('STATUS_QUEUED', STATUS_QUEUED)
print('STATUS_ACTIVE', STATUS_ACTIVE)
print('STATUS_SUCCESS', STATUS_SUCCESS)
print('STATUS_FAILED', STATUS_FAILED)
print('STATUS_COMPLETE', STATUS_COMPLETE)


# utils
def colorNote(txt, color=False, bg=False, bold=False):
	color = color if color else random.randint(1, 125)
	bg = bg if bg else random.randint(100, 255)
	color_code = '\033[38;5;%dm' % color
	bg_code = '\033[48;5;%dm' % bg if bg else ''
	print(color_code + bg_code + txt + '\033[0m')

CMD_CAPTURES = {
	'i': [
		r'^You are (unburdened|burdened) \((?P<burden>\d+)\%\) by\:$',
		r'^Holding \: (((?P<left>.+)) \(left hand\)|)((( and |)(?P<right>.+)) \(right hand\)\.$|)',
		r'^Wearing \: (?P<wearing>.+)\.$',
		r'^\(under\) \: (?P<under>.+)\.$',
		r'^Carrying\: (?P<carrying>.+)\.$',
		r'^Your purse contains (?P<purse>.+)\.$'
	],
	'l': [
		r'{"identifier":"(?P<identifier>.+)","name":"(?P<name>.+)","visibility":(?P<visibility>\d+),"kind":"(?P<kind>.+)"}$',
		r'^\[(?P<shortname>.+)\]$',
		#r'^.{1,10}$',
		r'^There are .+ obvious exit(s|)\: (?P<exits>.+)\.$',
	]
}

# aliases for directionals
CMD_CAPTURES['n'] = CMD_CAPTURES['l']
CMD_CAPTURES['nw'] = CMD_CAPTURES['l']
CMD_CAPTURES['ne'] = CMD_CAPTURES['l']

CMD_CAPTURES['s'] = CMD_CAPTURES['l']
CMD_CAPTURES['sw'] = CMD_CAPTURES['l']
CMD_CAPTURES['se'] = CMD_CAPTURES['l']

CMD_CAPTURES['e'] = CMD_CAPTURES['l']
CMD_CAPTURES['w'] = CMD_CAPTURES['l']

# queue of commands waiting to run...
CMDS = []
HISTORY = []

# handle input from the player
# manage initial queueing of commands...
def handleCommandSent(packet):

	new_cmd = {
		'cmd_txt': packet['cmd_txt'],
		'received': packet['received'],
		'completed': False
	}
	
	if new_cmd['cmd_txt'] in CMD_CAPTURES:
		queueCommand(new_cmd)
		
# add a command to global CMDS queue
def queueCommand(cmd):
	print('queueCommand', cmd['cmd_txt'])
	cmd['status'] = STATUS_QUEUED
	cmd['captures'] = CMD_CAPTURES[cmd['cmd_txt']]
	cmd['captured'] = {}
	cmd['response'] = []
	CMDS.append(cmd)

def handleTxtReceived(packet):

	# get line text
	sText = packet['txt']
	
	if CMDS:

		start_capture = CMDS[0]['captures'][0] if CMDS[0]['captures'] else False

		# is this the start? (assume it is not also the end)
		if start_capture and re.match(start_capture, sText):
			CMDS[0]['status'] = STATUS_ACTIVE
		
		# is this the end?
		if CMDS[0]['status'] == STATUS_ACTIVE:
			CMDS[0]['response'].append(sText)
			
			stop_capture = CMDS[0]['captures'][-1]
			
			if stop_capture and re.match(stop_capture, sText):
				CMDS[0]['captured'] = getCaptured(CMDS[0]['captures'], CMDS[0]['response'])
				CMDS[0]['status'] = STATUS_SUCCESS
				CMDS[0]['completed'] = packet['received']
				HISTORY.append(CMDS[0])
				
				colorNote('CAPTURED!')
				for k in CMDS[0]['captured']:
					print(k.upper()+':', CMDS[0]['captured'][k])
				
				CMDS.pop(0)


def getCaptured(captures, lines):
	
	all_captured = {}
	
	for line in lines:
		for regex in captures:
			result = re.search(regex, line)
			if result:
				groups = result.groupdict()
				captured = {k:v for k,v in groups.items() if v is not None}
				all_captured.update(captured)
	
	return all_captured


def START():
	# basic stats
	print('PLAYER:')
	print('SESSION START:')
	print('\n\n\n')
	
	# runs forever
	while True:
		for packet in tail('-f', '/home/zaya/Apps/MUSHclient/x/sync.in', _iter=True):

			data = json.loads(packet)
			if 'cmd_txt' in data:
				handleCommandSent(data)
				
			if 'txt' in data:
				handleTxtReceived(data)

START()