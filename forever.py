# python packages
from sh import tail
import json
import re

# my includes
from agent import Agent
from environment import Environment


# queue of commands waiting for captures
CMD_QUEUE = []
CMD_HISTORY = []

# output directly from the MUD client
LOG_FILE = '/home/zaya/Apps/MUSHclient/x/sync.in'

# messages from python bot to client
MSG_FILE = 'data/messages.json'

### GOAL CHECKS
# TODO: decide where to actually put this...
# represent each goal as its desired end state.

# search graph for unexpanded nodes
def is_expanded(graph):
	for node in self.GRAPH:
		for edge in node.edges:
			if not edge:
				return False
	return True
### END GOAL CHECKS


			
if __name__ == "__main__":
	
	# init a player agent
	player = Agent({
		'name': 'Zaya', 
		'goal': is_expanded
	})
	
	# place agent in environment
	game = Environment({'agent':player})
	
	# let's go!!
	game.start()

