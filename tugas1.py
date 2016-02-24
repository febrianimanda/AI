import csv

class Vertex:
	def __init__(self, node, heuristic = 0):
		self.id = node
		self.adjacent = {}
		self.heuristic = heuristic

	def __str__(self):
		# return 'vertex ' + str(self.id) + ' menuju -> ' + str([x.id for x in self.adjacent])
		return 'vertex ' + str(self.id)

	def __repr__(self):
		return self.__str__()

	def add_neighbor(self, neighbor, weight = 0):
		self.adjacent[neighbor] = weight

	def get_connections(self):
		return self.adjacent.keys()

	def get_id(self):
		return self.id

	def get_heuristic(self):
		return self.heuristic

	def get_weight(self, neighbor):
		return self.adjacent[neighbor]

	def is_connected(self):
		return bool(self.adjacent)

class Graph:

	def __init__(self):
		self.list_vertex = {}
		self.sum_vertex = 0

	def __iter__(self):
		return iter(self.list_vertex)

	#Fungsi untuk menambahkan vertex ke dalam graph
	def add_vertex(self, node, heuristic):
		self.sum_vertex = self.sum_vertex + 1
		new_vertex = Vertex(node, heuristic)
		self.list_vertex[node] = new_vertex
		return new_vertex

	#Fungsi untuk mengambil vertex dengan index n di dalam graph
	def get_vertex(self, n): 
		if n in self.list_vertex:
			return self.list_vertex[n]
		else:
			return None

	#fungsi untuk menambah arah dari 'src' ke 'dest' dengan biaya 'cost'
	def add_edge(self, src, dest, cost = 0): 
		#mengecek apakah source ada di dalam graph. Jika tidak ada maka akan ditambah di graph
		if src not in self.list_vertex:
			self.add_vertex(src)
		#mengecek apakah dest ada di dalam graph. Jika tidak ada maka akan ditambah di graph
		if dest not in self.list_vertex:
			self.add_vertex(dest)

		self.list_vertex[src].add_neighbor(self.list_vertex[dest], cost)

	#Fungsi untuk mengambil list dari vertex yang terdapat didalam graph
	def get_vertices(self):
		return self.list_vertex.keys()

	def heuristic_search(self, frm, dest):
		found = False
		closedlist = []
		current_cost = 0
		while not found:
			current_vertex = self.get_vertex(frm)
			current_cost += current_vertex.get_weight()
			f  = current_cost + current_vertex.get_heuristic()




if __name__ == '__main__':

	g = Graph()

	g.add_vertex('a', 0)
	g.add_vertex('b', 10)
	g.add_vertex('c', 5)
	g.add_vertex('d', 7)
	g.add_vertex('e', 8)
	g.add_vertex('f', 4)

	g.add_edge('a', 'b', 7)  
	g.add_edge('a', 'c', 9)
	g.add_edge('a', 'f', 14)
	g.add_edge('b', 'c', 10)
	g.add_edge('b', 'd', 15)
	g.add_edge('c', 'd', 11)
	g.add_edge('c', 'f', 2)
	g.add_edge('d', 'e', 6)
	g.add_edge('e', 'f', 9)

	# for v in g:
	print g.get_vertices()
	vert = g.get_vertex('a')
	print vert.get_connections()