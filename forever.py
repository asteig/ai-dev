from sh import tail
import json
import re 

STATUS_QUEUED = 'queued'
STATUS_ACTIVE = 'active'
STATUS_COMPLETE = 'complete'

# because I like my globals. :)
CMD_CAPTURES = {
	'i': [
		r'^You are (unburdened|burdened) \((?P<burden>\d+)\%\) by\:$',
		r'^Holding \: (((?P<left>.+)) \(left hand\)|)((( and |)(?P<right>.+)) \(right hand\)|)',
		r'^Wearing \: (?P<wearing>.+)\.$',
		r'^\(under\) \: (?P<under>.+)\.',
		r'^Carrying\: (?P<carrying>.+)\.',
		r'^Your purse contains (?P<purse>.+)\.'
	],
	'l': [
		r'^\[(?P<shortname>.+)\]$',
		r'^.{10}$',
		r'^There are .+ obvious exit(s|)\: (?P<exits>.+)\.$'
	]
}

# queue of commands waiting to run...
CMDS = []
HISTORY = []

# handle input from the player
def handleInput(packet):

	# add to queue
	# TODO: double check 2 packets dont come in at once (although sessions....)
	cmd = packet['cmd']

	# just humor two fake test commands...
	if cmd not in CMD_CAPTURES:
		return False

	if cmd in CMD_CAPTURES:
		captures = CMD_CAPTURES[cmd]
	else:
		captures = []
	
	CMDS.append({
		'cmd': cmd,
		'received': packet['received'],
		'completed': False,
		'started': False,
		'status': STATUS_QUEUED,
		'captures': captures,
		'captured': {}
	})
		

# handle response from the server
def handleOutput(packet):

	# get line text
	sText = packet['txt']
	
	# get active command (if any)
	if len(CMDS) > 0:
		cmd = CMDS[0]
		
		# your turn, bro!!!
		if cmd['status'] == STATUS_QUEUED:
			print('NEW COMMAND:', cmd['cmd'])
			cmd['status'] == STATUS_ACTIVE
		
		captures = cmd['captures']
		
		# no more captures means command received its expected response
		if len(captures) == 0:
			print('== COMPLETED CAPTURE:', CMDS[0]['captured'])
			cmd['status'] = STATUS_COMPLETE
			cmd['completed'] = packet['received']
			# move completed command to history...
			CMDS.pop(0)
			HISTORY.append(cmd)
		
		# one of more command captures left
		if len(captures) > 0:
			print(sText)
			captured = getCaptured(captures[0], sText)
			if captured:
				CMDS[0]['captured'].update(captured)
				CMDS[0]['captures'].pop(0)


def getCaptured(regex, txt):
	result = re.search(regex, txt)
	if result:
		captures = result.groupdict()
		return {k:v for k,v in captures.items() if v is not None}
	else:
		return False


def START():
	# runs forever
	while True:
		for line in tail('-f', '/home/zaya/Apps/MUSHclient/x/sync.io', _iter=True):

			data = json.loads(line)

			if 'cmd' in data:
				handleInput(data)
				
			if 'txt' in data:
				handleOutput(data)

print('FOREVER FILE!!!!!')
START()