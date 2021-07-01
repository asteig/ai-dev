import re

STATUS_QUEUED = "queued"
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'

REGEX_FAILED = r'(That doesn\'t work\.$|Try something else\.$|What\?$)'

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

CMD_CAPTURES['forward'] = CMD_CAPTURES['l']
CMD_CAPTURES['backward'] = CMD_CAPTURES['l']

CMD_CAPTURES['left'] = CMD_CAPTURES['l']
CMD_CAPTURES['right'] = CMD_CAPTURES['l']

CMD_CAPTURES['out'] = CMD_CAPTURES['l']

# TODO: make multi-line capture (one query)
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
	
def onCaptured(captured):
	print('i captured stuff... now what?')