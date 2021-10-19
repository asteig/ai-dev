STATUS_QUEUED = 'queued'
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'

class Mission:
	
	# hold all task-related data
	data = {}
	
	# hold all relevent data from the database
	memo = {}
	
	def __init__(self):
		self.actions = [m for m in dir(self) if not m.startswith('_') and m.endswith('_')]
		print(self.actions)

	# look for any command handlers
	# TODO: this actually working... LOL
	def next(self, percept):
		meth_name = percept['action']+'_'
		if meth_name in self.actions:
			meth = getattr(self, meth_name)
			meth(self, **{'data': percept})

	def memo(self, data):
		print('REMEMBER----------')
		for attr in self.data:
			print(attr, data)
		print('------------------')
		
		
'''
frontier = []

explored = {}

def addNode(node)
	explored[node.id] = node
	for edges in node.edges:
		frontier[] = node.id + edge
'''
	
		
