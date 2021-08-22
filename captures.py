# matches everything EXCEPT player commands
REGEX_RESPONSE = r'^[\WA-Z]'

# matches basic user input (editors, etc. handled separately)
REGEX_COMMAND = r'^[a-z]'

# matches any error text
REGEX_FAILED = r'(?P<failed>(^That doesn\'t work\.$|^Try something else\.$|What\?$))'

CMD_CAPTURES = {
	'inventory': [
		r'^You are (unburdened|burdened) \((?P<burden>\d+)\%\) by\:$',
		r'^Holding \: (((?P<left>.+)) \(left hand\)|)((( and |)(?P<right>.+)) \(right hand\)\.$|)',
		r'^Wearing \: (?P<wearing>.+)\.$',
		r'^\(under\) \: (?P<under>.+)\.$',
		r'^Carrying\: (?P<carrying>.+)\.$',
		r'(^Your purse contains (?P<purse>.+)\.$|^You are just a disembodied (?P<dead>spirit))'
	],
	# TODO: p-shop browse as well
	'list': [
		r'^The following items are for sale:$',
		r'^   (?P<id>.+)\: (?P<item>.+) for (?P<price>.+) \(.+\)\.$',
		r'(?!^   (?P<id>.+)\: (?P<item>.+) for (?P<price>.+) \(.+\).*$'
	],
	'locate': [
		r'^The (?P<item>.+) \((?P<id>\d+)\) is (?P<location>.+$).',
		r'^(?!^The .+ \(\d+\) is (?P<location>.+)).*'
	],
	'look': [
		# TODO: parse any json...
		#r'{\"identifier\":\"(?P<identifier>.+)\",(\"tz\":(?P<tz>.+),|)\"name\":\"(?P<name>.+)\",(\"ty\":(?P<ty>\d+),|)(\"terrain\":(?P<terrain>.+),|)\"visibility\":(?P<visibility>\d+),(\"tx\":(?P<tx>.+),|)\"kind\":\"(?P<kind>.+)\"}$',
		r'(?P<room_json>{\"identifier\".+$)',
		r'^\[(?P<room_name>.+)\]$',
		r'^There (is|are) .+ obvious exit(s|)\: (?P<room_exits_list>.+)\.$'
	]
}

CMD_ALIASES = {
	'look': [
		'l',
		'n', 's', 'e', 'w', 
		'forward', 'backward',
		'left', 'right',
		'up', 'down',
		'out',
	],
	'inventory': ['i']
}



RESPONSE_CAPTURES = {
	'prompt': [
		r'(?P<prompt>^.+(\:$|\? ))(\((?P<options>.+)\)$|)',
		r'(^(?P<response>[a-z].+)|^(?P<failed>[\WA-Z].+))'
	],
	'stats': [
		r'{\"alignment\":\"(?P<alignment>.+)\",\"maxhp\":(?P<maxhp>\d+),\"hp\":(?P<hp>\d+),\"xp\":(?P<xp>\d+),\"maxgp\":(?P<maxgp>\d+),\"burden\":(?P<burden>\d+),\"gp\":(?P<gp>\d+)}',
	]
}
