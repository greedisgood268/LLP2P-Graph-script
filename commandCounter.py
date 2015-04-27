import re
import sys

def parseFile(name):
	fileName = name 
	readFile = open(fileName,'r')
	currentMinute = 0 
	currentSecond = 0 
	cluster = {}

	for line in readFile:
		time = re.findall('[0-9]{1,9}',line)
		time = map(int,time)
		minute = time[0]
		second = time[1]
		miniSecond = time[2]
		if cluster.has_key(minute):	
			data = cluster[minute]
			if second > 30 or (second == 30 and miniSecond > 0):
				if len(data) < 2:
					data.append(1)
				else:
					data[1] += 1
			else:
				data[0] += 1
		else:
			data = []	
			if second < 30:
				data.append(1)
			else:
				data.append(0)
				data.append(1)
			cluster[minute] = data
	index = cluster.keys()
	value = sorted(index)
	if len(value) == 0:
		return
	maxMinute = value[len(value)-1]

	for a in range(0,maxMinute+1):
		if cluster.has_key(a):
			data = cluster[a]
			if len(data) == 2:
				print data[0]
				print data[1]
			else:
				print data[0]
				print 0
		else:
			print 0
			print 0

if __name__ == '__main__':
	if len(sys.argv) == 2:
		parseFile(sys.argv[1])
	else: 
		print 'Failed command'
#print '-----------------------------end--------------------------',maxMinute
#for key in value:
#	print key,cluster[key]
