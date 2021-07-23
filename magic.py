### MAGIC COMMANDS
MAP_START = False
MAP_HISTORY = []
# just for development...
def _mapStart(graph):
	print('_mapStart')
	MAP_START = True
	return graph
	
def _mapShow(graph):
	print('_mapShow')
	
	if not graph:
		return False
	
	# TODO: less sloppy bounding...
	# make sure the grid is big enough...
	offset_x = abs(min([graph[n_id].x for n_id in graph])) + 5
	offset_y = abs(min([graph[n_id].y for n_id in graph])) + 5
	
	# make [y][x] grid with a width of 13
	display_grid = []
	for y in range(0, (20)):
		row = [' '] * (20)
		display_grid.append(row)

	for node_id in graph:
		node = graph[node_id]
		display_grid[node.y+offset_y][node.x+offset_y] = '#' if node.expanded else 'X'
		
	for row in display_grid:
		print(''.join(row))

def _mapStop(graph):
	print('_mapStop')
	MAP_START = False
	return graph
	
def _mapReset(graph):
	print('_mapReset')
	return []
	
# print data out using aima data representations... 
def _mapPrint(graph):
	flat_graph = []
	for node_id in graph:
		node = graph[node_id]
		flat_graph.append({
			'id': node.id,
			'parent_id': node.parent_id,
			'action': node.action,
			'path_cost': node.path_cost,
			'edges': node.edges
		})
	print('---graph data structure:')
	print(flat_graph)
	print('---')
	return graph
	
def _mapSave(graph):
	print('Save JSON data:')
	print(json.dumps(graph))
	print('--------------')

####### next
# recommend next action...
# (next unexplored action, closest to current position)
def _mapNext(graph):
	print('_mapNext')

	
# TODO: make dynamic...
MAGIC_PHRASES = {
	'You exclaim: START!!': _mapStart,
	'You exclaim: SHOW!!': _mapShow,
	'You exclaim: STOP!!': _mapStop,
	'You exclaim: RESET!!': _mapReset,
	'You exclaim: PRINT!!': _mapPrint,
	'You exclaim: SAVE!!': _mapSave,
	'You exclaim: NEXT!!': _mapNext
}
	
### END MAGIC COMMANDS