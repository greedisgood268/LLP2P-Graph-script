#firstTime = raw_input('Input the first time to compare:\n')
#secondTime = raw_input('Input the second time to compare:\n')
#firstTime = 2
#secondTime = 4
import sys

class Maximum(object):
	
	def __init__(self):
		self.maximum = [0.00,0.00,0.00,0.00,0.00]

	def printMaximum(self): 
		print self.maximum

	def setMaximum(self,subStreamId, delay): 
		if self.maximum[subStreamId] < delay:
			self.maximum[subStreamId] = delay

	def getMaximum(self,subStreamId): 
		return self.maximum[subStreamId]

	def resetMaximum(self): 
		self.maximum = [0.00,0.00,0.00,0.00,0.00]


def parseFile(command):

	fileName = 'client_data_of_chn_1.txt'
	readFile = open(fileName,'r')
	value = [0.00,0.00,0.00,0.00,0.00]
	time = 0
	currentCheck = -1
	maximum = Maximum()

	for line in readFile:
		result = line.split()
		if currentCheck != int(result[0]):
			printValue = [0.00,0.00,0.00,0.00,0.00]
			for streamIndex in range(0,5):
				if currentCheck != -1:
					printValue[streamIndex] = value[streamIndex]/time	

				value[streamIndex] = (float)(result[ 4 + streamIndex])
				maximum.setMaximum(streamIndex,value[streamIndex]);
			if currentCheck != -1:
				if command != -1:
					print maximum.getMaximum(command)
			currentCheck = int(result[0])
			time = 1
			maximum.resetMaximum()
		else:
			for streamIndex in range(0,5):
				value[streamIndex] += (float)(result[ 4 + streamIndex])
				maximum.setMaximum(streamIndex,value[streamIndex]);
			time = time + 1 
		
	readFile.close()	

if __name__ =='__main__':

	if len(sys.argv) > 1:
		parseFile(int(sys.argv[1]))
	else:
		parseFile(-1)

