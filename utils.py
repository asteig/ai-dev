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