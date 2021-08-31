# matches everything EXCEPT player commands
REGEX_RESPONSE = r'^[\WA-Z]'

# matches basic user input (editors, etc. handled separately)
REGEX_COMMAND = r'^[a-z]'

# matches any error text
REGEX_FAILED = r'(?P<failed>(^That doesn\'t work\.$|^Try something else\.$|What\?$))'

CMD_CAPTURES = {
	'inventory': [
		r'^You are (unburdened|burdened) \((?P<inventory_burden>\d+)\%\) by\:$',
		r'^Holding \: (((?P<inventory_left>.+)) \(left hand\)|)((( and |)(?P<inventory_right>.+)) \(right hand\)\.$|)',
		r'^Wearing \: (?P<inventory_wearing_list>.+)\.$',
		r'^\(under\) \: (?P<inventory_under_list>.+)\.$',
		r'^Carrying\: (?P<inventory_carrying_list>.+)\.$',
		r'(^Your purse contains (?P<inventory_purse_list>.+)\.$|^You are just a disembodied (?P<char_dead>spirit))'
	],
	# TODO: p-shop browse as well
	'list': [
		r'^The following items are for sale:$',
		r'^   (?P<id>.+)\: (?P<item>.+) for (?P<price>.+) \(.+\)\.$',
		r'^(.+) list From \d+ to \d+ of (?P<shop_total>\d+)',
		#r'(?!^   (?P<id>.+)\: (?P<shop_item>.+) for (?P<price>.+) \(.+\).*$)',
		r'^(?P<shop_keeper>.+) (says|exclaims|asks)\: (.+)$'
	],
	'locate': [
		r'^The (?P<item>.+) \((?P<id>\d+)\) is (?P<location>.+)\.$',
		r'^(?!^The .+ \(\d+\) is .+).*'
	],
	'look': [
		# TODO: parse any json...
		#r'{\"identifier\":\"(?P<identifier>.+)\",(\"tz\":(?P<tz>.+),|)\"name\":\"(?P<name>.+)\",(\"ty\":(?P<ty>\d+),|)(\"terrain\":(?P<terrain>.+),|)\"visibility\":(?P<visibility>\d+),(\"tx\":(?P<tx>.+),|)\"kind\":\"(?P<kind>.+)\"}$',
		r'(?P<room_json>{\"identifier\".+$)',
		r'^\[(?P<room_name>.+)\]$',
		r'^There (is|are) .+ obvious exit(s|)\: (?P<room_exits_list>.+)\.$'
	],
	'value': [
		r'^You estimate that the (?P<value_item>.+) is worth (?P<value_amount>.+)\.  ',
		r'^(?!You estimate that the .+ is worth .+\.)'
	],
	'help': {
		r'((?P<help_type>.+) \b\w+\b room help|((?P<failed>There is no help available for this room\.$))',
		r'(\w.+ - (?P<help_description>.+)',
		r'^\ {5}(?P<help_cmd>\w+) (?P<help_syntax>([^\w]).+)',
		r'^See also'
	}
	
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
	'inventory': ['i'],
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
