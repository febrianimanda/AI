import csv
import itertools

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
      if valArr == i[0:3]:
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

  def collecting(self, f):
    coll = []
    coll.append(f['STG'].keys())
    coll.append(f['SCG'].keys())
    coll.append(f['PEG'].keys())
    return coll

  def inference(self, fuzVal):
    coll = [b for b in itertools.product(*self.collecting(fuzVal))]
    lencombi = len(coll)
    comb = {}
    result = []
    for i in range(lencombi):
      member = [x for x in coll[i]]
      value = [fuzVal['STG'][member[0]], fuzVal['SCG'][member[1]], fuzVal['PEG'][member[2]]]
      comb[i] = {
        'min' : min(value),
        'rulesres': self.getRulesResult(member)
      }
    return comb

  def deffuzzication(self, infVal):
    sugeno = {'vl': 0, 'l': 1, 'm': 2, 'h': 3}
    result = {}
    for i in range(len(infVal)):
      infVal[i]['sugeno'] = sugeno[infVal[i]['rulesres']] * infVal[i]['min']
    result = {}
    divider = {}
    for i in range(len(infVal)):
      if infVal[i]['rulesres'] in result.keys():
        if result[infVal[i]['rulesres']] < infVal[i]['sugeno']:
          result[infVal[i]['rulesres']] = infVal[i]['sugeno']
          divider[infVal[i]['rulesres']] = infVal[i]['min']
      else:
        result[infVal[i]['rulesres']] = infVal[i]['sugeno']
        divider[infVal[i]['rulesres']] = infVal[i]['min']
    total = round(sum(result.values()) / sum(divider.values()))
    return 'very_low' if total == 0 else 'Low' if total == 1 else 'Middle' if total == 2 else 'High'

  def cekAccurate(self, defuzVal, index, acc):
    result = 1 if data[index]['UNS'] == defuzVal else 0
    acc += result
    if index < 10:
      zero = '00'   
    elif index < 100:
      zero = '0'
    else:
      zero = ''
    print '%s%s : %s' % (zero, index, 'T' if data[index]['UNS'] == defuzVal else 'F'), '\t|','\t%.2f%%' % (0 if acc == 0 else float(acc) / float(len(data)) * 100)
    # print data[index]['UNS'], defuzVal, '=', data[index]['UNS'] == defuzVal, '\t result',0 if acc == 0 else float(acc) / float(len(data)) * 100,'%'
    return result

fuzzy = Fuzzy()
trueval = 0

print 'Progress \t|\t Accuracy'

for i in data:
  fuz = fuzzy.fuzzication(data[i])
  infer = fuzzy.inference(fuz)
  defuz = fuzzy.deffuzzication(infer)
  trueval += fuzzy.cekAccurate(defuz, i, trueval)

print 'Final Accuracy = ', '%.2f%%' % (float(trueval) / float(len(data)) * 100)