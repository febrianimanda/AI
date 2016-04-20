import csv

data = {}

with open('Dataset.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  i = 0
  for row in reader:
    data[i] = {
    	'STG' : row[0],
    	'SCG' : row[1],
    	'PEG' : row[4],
    	'UNS' : row[5]
    }
    i += 1

print data