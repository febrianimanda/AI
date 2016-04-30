import csv, math
import numpy as np

data = {}
target = []
with open('occupancy.csv', 'rb') as csvfile:
  reader = csv.DictReader(csvfile, delimiter=',')
  i = 0
  for row in reader:
    data[i] = [float(row['Temperature']), float(row['Humidity']), float(row['Light']), float(row['CO2'])]
    target.append(int(row['Occupancy']))
    i += 1

class Neuron:

	def __init__(self, x, w):
		self.w = w
		self.x = x
		self.summingval = self.summming()

	def summming(self):
		result = 0
		if isinstance(self.x, list):
			for i in range(len(self.x)):
				result += self.x[i] * self.w[i]
		else:
			result = self.x * self.w
		return result

	def aktivasi(self):
		return 1/(1+math.exp(-self.summingval))

class JST:
	
	def __init__(self, data, target, epoch):
		self.jInput = 4
		self.jNeuron = 4
		self.lendata = len(data)
		self.lentarget = len(target)
		self.learningrate = 0.1
		self.data = data
		self.target = target
		self.epoch = epoch
		self.MSE = []
		self.w1 = np.random.uniform(-.1,.1,self.jNeuron*4)
		self.w2 = np.random.uniform(-.1,.1,self.jNeuron)

	def running(self):
		ee = 0
		while ee < self.epoch:
			MSEepoch = 0
			for index in range(self.lendata):
				print ee, index
				#Forwarding
				##Hidden Layer
				nHidden = []
				for i in range(self.jNeuron):
					a,b = i * self.jNeuron, (i+1) * self.jNeuron
					neuron = Neuron(self.data[index], self.w1[a:b])
					nHidden.append(neuron.aktivasi())
				
				##Output Neuron
				neuron = Neuron(nHidden, self.w2)
				nOutput = neuron.aktivasi()

				##collecting error
				err = self.target[index] - nOutput
				##Calculating MSE
				MSEepoch = MSEepoch + (err**2)
				
				#Back Propagation
				d2 = nOutput * (1-nOutput) * err
				dw2 = []
				for i in range(self.jNeuron):
					dw2.append(self.learningrate * d2 * nHidden[i])

				d1 = []
				for i in range(self.jNeuron):
					d1.append(nHidden[i] * (1-nHidden[i]) * d2 * self.w2[i])

				dw1 = []
				for i in range(self.jInput):
					delta1 = []
					for j in range(self.jNeuron):
						delta1.append(self.learningrate * d1[j] * data[index][j])
					dw1.append(delta1)
				
				for i in range(len(dw1)):
					for j in range(len(dw1[i])):
						self.w1[i*j] = self.w1[i*j] + dw1[i][j]
				self.w2 = [x+y for x,y in zip(self.w2, dw2)]

			ee += 1
			self.MSE.append(MSEepoch/self.lendata)

print np.random.uniform(-1,1,10,5)
# jst = JST(data, target, 100)
# jst.running()
# for i in jst.MSE:
# 	print i
# print len(data)
# print jst.MSEepoch
# a = [1,2,3,4]
# b = [2,3,4,5]
# c = [x + y for x, y in zip(a, b)]