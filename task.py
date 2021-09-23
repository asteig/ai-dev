from tasks.mccounter import *

class Task:
	
	def __init__(self, task_name):
		print('TASK', task_name)
		self.current = self._load(task_name)
		self.actions = [m for m in dir(self.current) if m == m.lower() and not m.startswith('__')]
		print('ACTIONS', self.actions)
		
	def _load(self, task_name):
		return McCounter

	def next(self, percept):
		meth_name = percept['action']+'_'
		if meth_name in self.actions:
			meth = getattr(self.current, meth_name)
			meth(self.current, **{'data': percept})
