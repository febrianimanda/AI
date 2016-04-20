# Name : Febrian Imanda Effendy
# NIM : 1103134334
# Kelas : IF-37-06
# Algoritma A* Heuristic Search dengan representasi graph

graph = {
	'Bobbia' : {
		'Terme' : 3,
		'Piacenza' : 5,
		'Cesena' : 15
	},
	'Piacenza' : {
		'Terme' : 3,
		'Carpi' : 3,
	},
	'Terme' : {
		'Emilia' : 2,
		'Faenza' : 3
	},
	'Carpi' : {
		'Emilia' : 2,
		'Ferrara' : 8
	},
	'Emilia' : {
		'Imola' : 2
	},
	'Imola' : {
		'Faenza' : 1,
		'Forli' : 3
	},
	'Forli' : {
		'Cesena' : 2,
		'Ravenna' : 3
	},
	'Faenza' : {
		'Forli' : 2,
		'Cesena' : 6
	},
	'Cesena' : {
		'Rimini' : 5
	},
	'Ferrara' : {
		'Imola' : 3,
		'Ravenna' : 6
	},
	'Rimini' : {
		'Ravenna' : 1	
	}
}

h = {
	'Ravenna' : 0,
	'Rimini' : 0.5,
	'Ferrara' : 5,
	'Forli' : 2,
	'Cesena' : 4.5,
	'Faenza' : 4,
	'Imola'	: 5,
	'Emilia' : 6,
	'Terme' : 7,
	'Carpi' : 8,
	'Piacenza' : 10,
	'Bobbia' : 10.5
}
closedlist = []
cost = 0

def heuristic_search(graph, start, end, closedlist, cost):
	closedlist.append(start)
	print 'Closedlist = ', closedlist
	print 'Biaya yang dibutuhkan saat ini = ', cost
	if start == end :
		print ''
		print '==================================='
		print ''
		print 'Rute yang ditemukan : ', closedlist
		print 'Biaya yang dibutuhkan : ', cost
	if not graph.has_key(start) :
		return 'Node ada yang tidak ditemukan'
	fmin = 100
	gmin = 100
	ntemp = start
	print ''
	print 'Open = ', graph[start].keys()
	for node in graph[start]:
		if not node in closedlist :
			gtemp = cost + graph[start][node]
			ftemp = gtemp + h[node]
			print 'Node',node,', f(',node,') = ',ftemp
			if ftemp < fmin : 
				fmin = ftemp
				gmin = gtemp
				ntemp = node
	cost = gmin
	heuristic_search(graph, ntemp, end, closedlist, cost)

start = 'Bobbia'
finish = 'Ravenna'
print "Start : ", start
heuristic_search(graph, start, finish, closedlist, cost)
