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

REGEX_FAILED = r'(That doesn\'t work\.$|Try something else\.$|What\?$)'

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

CMD_CAPTURES['up'] = CMD_CAPTURES['l']
CMD_CAPTURES['down'] = CMD_CAPTURES['l']

# queue of commands waiting to run...
CMDS = []
HISTORY = []

# handle input from the player
# manage initial queueing of commands...
def handleCommandSent(packet):

	cmd_txt = packet['cmd_txt']
	
	if cmd_txt in CMD_CAPTURES:
		new_cmd = {
			'cmd_txt': cmd_txt,
			'received': packet['received'],
			'status': STATUS_QUEUED,
			'captures': CMD_CAPTURES[cmd_txt],
			'response': [],
			'captured': {},
			'completed': False
		}
		print('queuing:', new_cmd['cmd_txt'])
		CMDS.append(new_cmd)

def handleTxtReceived(packet):

	# get line text
	sText = packet['txt']
	
	# return False if there's no commands in the queue to process...
	if not CMDS:
		return False

	next_cmd = CMDS[0]
	
	# command doesn't work...
	if re.search(REGEX_FAILED, sText):
		next_cmd['status'] = STATUS_FAILED
		next_cmd['completed'] = packet['received']
		HISTORY.append(next_cmd)
		CMDS.pop(0)
		return False
	
	start_capture = next_cmd['captures'][0]
	stop_capture = next_cmd['captures'][-1]
	
	if re.search(start_capture, sText):
		colorNote('START CAPTURING!!!!!')
		next_cmd['status'] = STATUS_ACTIVE
	
	if next_cmd['status'] == STATUS_ACTIVE:
		# add this line to the response
		next_cmd['response'].append(sText)
		
	if re.search(stop_capture, sText):
		colorNote('********* CAPTURED DATA:')
		captured = getCaptured(next_cmd['captures'], next_cmd['response'])
		print(captured)
		print('')
		print('')
		print('')
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