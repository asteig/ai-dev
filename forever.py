from sh import tail
import json
import re 
import utils 

STATUS_QUEUED = 'queued'
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'

# utils
def colorNote(txt, color=12, bg=False, bold=False):
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
	print(packet['cmd'])
	# add to queue
	# TODO: double check 2 packets dont come in at once (although sessions....)
	cmd = packet['cmd']
	print('queueing the command.....', cmd)
	
	if cmd not in CMD_CAPTURES:
		colorNote('WARNING: No captures for this command!')

	# add new command to cmd queue
	CMDS.append({
		'cmd': cmd,
		'received': packet['received'],
		'completed': False,
		'status': STATUS_QUEUED,
		'captures': CMD_CAPTURES[cmd] if cmd in CMD_CAPTURES else False,
		'captured': {},
		'response': []
	})

def handleTxtReceived(packet):
	# get line text
	sText = packet['txt']
	
	active_command = CMDS[0] if CMDS else False
	
	# get active command capture
	if active_command:
		
		# did the command fail?
		result = re.match(r'(^What\?$|^Try something else.$|^That doesn\'t work.$)', sText)
		if result:
			colorNote('COMMAND FAILED: ' + CMDS[0]['cmd'])
			active_command['status'] = STATUS_FAILED
			active_command['completed'] = packet['received']
			HISTORY.append(active_command)
			CMDS.pop(0)
			return False
		
		# if the command already started...
		active_command['response'].append(sText)
		
		stop_capture = active_command['captures'][-1] if active_command['captures'] else False
		
		# is this the last capture?
		if stop_capture and re.match(stop_capture, sText):
			colorNote('ENDING! FULL RESPONSE:', 12, 1)

			active_command['status'] = STATUS_SUCCESS
			active_command['completed'] = packet['received']
			
			# get captures:
			captured = getCaptured(active_command['captures'], active_command['response'])
			print('CAPTURED!!!!!', captured)
			
			HISTORY.append(active_command)
			CMDS.pop(0)


def getCaptured(captures, lines):
	
	print('getCaptured:')
	[print(line) for line in lines]
	
	all_captured = {}
	
	for line in lines:
		for regex in captures:
			result = re.search(regex, line)
			if result:
				groups = result.groupdict()
				captured = {k:v for k,v in groups.items() if v is not None}
				all_captured.update(captured)
				if captures:
					captures.pop(0)
	
	return all_captured


def START():
	# basic stats
	print('PLAYER:')
	print('SESSION START:')
	print('\n\n\n')
	
	# runs forever
	while True:
		for line in tail('-f', '/home/zaya/Apps/MUSHclient/x/sync.in', _iter=True):

			data = json.loads(line)

			if 'cmd' in data:
				handleCommandSent(data)
				
			if 'txt' in data:
				handleTxtReceived(data)

START()