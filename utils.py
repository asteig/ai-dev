import random

# utils
def colorNote(txt, color=False, bg=False, bold=False):
	color = color if color else random.randint(1, 125)
	bg = bg if bg else random.randint(100, 255)
	color_code = '\033[38;5;%dm' % color
	bg_code = '\033[48;5;%dm' % bg if bg else ''
	print(color_code + bg_code + txt + '\033[0m')
	
def splitList(txt):
	txt = txt.replace(' and ', ', ')
	items = txt.split(', ')
	return items
	
direction_alias = {
	'north': 'n',
	'south': 's',
	'east': 'e',
	'west': 'w',
	'northeast': 'ne',
	'northwest': 'nw',
	'southeast': 'se',
	'southwest': 'sw',
	# 'up': 'up',
	# 'down': 'down'
}

alias_direction = {v: k for k, v in direction_alias.items()}

REVERSE_ACTION = {
	'n': 's',
	's': 'n',
	'e': 'w',
	'w': 'e',
	'ne': 'sw',
	'nw': 'se',
	'se': 'nw',
	'sw': 'ne',
	'l': 'l'
	# 'up': 'down',
	# 'down': 'up'
}