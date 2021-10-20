STATUS_QUEUED = 'queued'
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'

class Mission:
	
	# hold all task-related data
	data = {}
	
	# hold all relevent data from the database
	memo = {}
	
	# keep track of all actions performed during the mission
	sequence = []
	
	def __init__(self):
		self.actions = [m for m in dir(self) if not m.startswith('_') and m.endswith('_')]
		print(self.actions)

	# look for any command handlers
	# TODO: this actually working... LOL
	def next(self, data):
		meth_name = data['action']+'_'
		if meth_name in self.actions:
			meth = getattr(self, meth_name)
			meth(self, **{'data': data})

	def memo(self, data):
		print('REMEMBER----------')
		for attr in self.data:
			print(attr, data)
		print('------------------')
