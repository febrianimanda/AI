import csv

data = {}
rules = []

with open('Dataset.csv', 'rb') as csvfile:
  reader = csv.DictReader(csvfile, delimiter=',')
  i = 0
  for row in reader:
    data[i] = {
      'STG' : float(row['STG']),
      'SCG' : float(row['SCG']),
      'PEG' : float(row['PEG']),
      'UNS' : row['UNS']
    }
    i += 1

with open('rules.csv', 'rb') as csvfile:
  reader = csv.DictReader(csvfile, delimiter=',')
  for row in reader:
    rules.append([row['a'], row['b'], row['c'], row['result']])

class Trapesium:
  def __init__(self, a, b, c, d):
    self.a = a
    self.b = b
    self.c = c
    self.d = d

  def setA(self, a):
    self.a = a

  def getA(self):
    return self.a

  def setB(self, b):
    self.b = b

  def getB(self):
    return self.b

  def setC(self, c):
    self.c = c

  def getC(self):
    return self.c

  def setD(self, d):
    self.d = d

  def getD(self):
    return self.d

  def calcValue(self, value):
    if value >= self.b and value <= self.c:
      return 1
    elif value > self.a and value < self.b:
      return (value - self.a) / (self.b - self.a)
    elif value > self.c and value < self.d:
      return -(value- self.d) / (self.d - self.c)
    else:
      return 0

class Fuzzy:
  def __init__(self):
    self.tLow = Trapesium(-.3,-.2,.2,.3)
    self.tMiddle = Trapesium(.2,.3,.7,.8)  
    self.tHigh = Trapesium(.7,.8,1.2,1.3)

  def getRulesResult(self, valArr):
    for i in rules:
      if valArr[0:3] == i[0:3]:
        return i[3]

  def fuzzication(self, dictValue):
    var = {'STG':{}, 'SCG':{}, 'PEG':{}}
    for key, value in dictValue.iteritems():
      l = self.tLow.calcValue(value)
      m = self.tMiddle.calcValue(value)
      h = self.tHigh.calcValue(value)
      if l > 0: var[str(key)]['l'] = l
      if m > 0: var[str(key)]['m'] = m
      if h > 0: var[str(key)]['h'] = h
    return var

  def inference(self, f):
    # print f.items()
    comb = {}
    length_dict = {key: len(value) for key, value in f.items()}
    mlen = max(length_dict.items(), key=lambda x: x[1])
    
    # print mlen 
    # for i in range(mlen[1]):
    #   comb.append([])
    
    comb[0].append(f['STG'].keys()[0])
    comb[0].append(f['SCG'].keys()[0])
    comb[0].append(f['PEG'].keys()[0])

    minval = {}
    for i in f[mlen[0]].keys():
      minval[i] = 99
      for j in f:
        if f[j].has_key(i):
          if f[j][i] < minval[i]:
            minval[i] = f[j][i]

    print minval

    if mlen[1] > 1:
      lenstg = len(f['STG'])
      lenscg = len(f['SCG'])
      lenpeg = len(f['PEG'])

      comb[1].append(f['STG'].keys()[1 if lenstg > 1 else 0])
      comb[1].append(f['SCG'].keys()[1 if lenscg > 1 else 0])
      comb[1].append(f['PEG'].keys()[1 if lenpeg > 1 else 0])

    print comb
    res = []
    for i in range(mlen[1]):
      res.append(self.getRulesResult(comb[i]))

    print res


      
  def deffuzzication(self):
    return True

f = Fuzzy()
a = f.fuzzication(data[4])
print a
f.inference(a)
# print a['PEG'].keys()

# print min(a.items(), key=lambda x: x[1])