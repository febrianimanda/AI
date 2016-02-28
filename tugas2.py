import csv, math, random
from operator import itemgetter

nodes = {}
with open('nodes.csv', 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	i = 0
	for row in reader:
		nodes[row['Node ']] = {
			'x' : row['x'],
			'y' : row['y'],
			'demand' : row['Demand']
		}

def distance(node1,node2):
	x = pow(float(node2['x'])-float(node1['x']),2)
	y = pow(float(node2['y'])-float(node1['y']),2)
	return pow(x+y,1/2.0)

def initKromosom(start):
	krom = nodes.keys()
	if start in nodes.keys() :
		krom.remove(start)
	else:
		del krom[0]
	random.shuffle(krom)
	return krom

def fitness(h):
	return 1/h

def getBackDistance(curNode):
	return distance(nodes[curNode], nodes[start])

def fitnessing(population):
	genFit = []
	distanceFit = []
	for i in range(nPop):
		demandTotal = int(nodes[population[i][0]]['demand'])
		distanceTotal = distance(nodes[populasi[i][0]], nodes[start])
		demandTemp = 0
		for j in range(nGen-1):
			demandTemp = int(nodes[population[i][j+1]]['demand'])
			if (int(demandTotal) + int(demandTemp)) > 100 :
				demandTotal = 0
				distanceTotal += getBackDistance(population[i][j])
				distanceTotal += getBackDistance(population[i][j+1])
			else :
				distanceTotal += distance(nodes[population[i][j]], nodes[population[i][j+1]])
			demandTotal += int(demandTemp)
			# print j, demandTotal, distanceTotal
		distanceTotal += getBackDistance(population[i][j+1])
		genFit.append(fitness(distanceTotal))
		distanceFit.append(distanceTotal)
	return [distanceFit, genFit]

def books(list1, list2):
	book = []
	for i in range(nPop):
		book.append({"Kromosom":list1[i], "Fitness":list2[i]})
	return book

def parentSelection(eraFit, rand): #seleksi orangtua
	total = 0
	for a in range(nPop):
		total += eraFit[a]
		if(total > rand):
			return a

def rouletteWheel(eraFit, population): #roulette wheel
	selected = []
	while len(selected) < 2:
		n = random.uniform(min(eraFit), sum(eraFit))
		selected.append(population[parentSelection(eraFit,n)])
	return selected

def crossover(par): #fungsi crossover
	silang = random.randint(0,1)
	if silang != 0 :
		titik = random.randint(0,31)
		child1 = [par[0][x] for x in range(titik)]
		child2 = [par[1][y] for y in range(titik)]
		for x in range(nGen):
			if par[1][x] not in child1:
				child1.append(par[1][x])
			if par[0][x] not in child2:
				child2.append(par[0][x])
	else :
		child1 = par[0]
		child2 = par[1]
	return [child1, child2]

def mutation(child):
	setMutation = 0.2
	for i in range(2):
		rand = random.uniform(0,1)
		if (rand < setMutation) :
			titik = random.sample(range(0,31), 2)
			child[i][titik[0]], child[i][titik[1]] = child[i][titik[1]], child[i][titik[0]]
	return child

def geneticAlgorithm(populasi, eraFit, bookPop):
	matingPool = []
	#seleksi Orang Tua
	for i in range(nPop/2):
		parent = rouletteWheel(eraFit, populasi)
		child = crossover(parent)
		child = mutation(child)
		matingPool.append(child)

	#seleksi survivor
	survivor = []
	for i in range(nPop/2):
		for j in range(2):
			survivor.insert(i, matingPool[i][j])
	survFungsi = fitnessing(survivor)
	genSurvivor = survFungsi[1]
	bookPop.extend(books(survivor,genSurvivor))
	bookPop = sorted(bookPop, key=itemgetter('Fitness'), reverse=True)
	for i in range(nPop):
		newPop.append(bookPop[i].values()[0])

# initial 
consDemand = 100
nPop = 10
nGen = 31
start = '0'
xStart = nodes[start]['x']
yStart = nodes[start]['y']
era = 0
newPop = []

for era in range(10000) :
	print "Generasi ", era+1
	populasi = newPop[:] if era > 0 else [initKromosom('0') for x in range(nPop)]
	# populasi = [[str(x) for x in range(1,32)] for y in range(1,3)]
	fungsi = fitnessing(populasi)
	eraDistance = fungsi[0]
	eraFit = fungsi[1]
	bookPop = books(populasi, eraFit)
	bestFit = populasi[eraFit.index(max(eraFit))]
	bestDistance = eraDistance[eraFit.index(max(eraFit))]

	print "Rute terbaik : ", bestFit
	print "Cost dari Rute Terbaik : ", bestDistance
	print "Rata-rata Fitness : ", sum(eraFit) / len(eraFit)
	print "Fitness Terbaik : ", max(eraFit)

	geneticAlgorithm(populasi, eraFit, bookPop)

	print "============================"

print 'Rute Terbaik : ',bestFit
print 'Cost dari Rute Terbaik : ', bestDistance