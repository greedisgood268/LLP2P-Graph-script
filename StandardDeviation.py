import sys
import math
class PeerDelay(object):

	def __init__(self,pid):

		self.maxDelay = 0
		self.delay1 = 0
		self.delay2 = 0
		self.delay3 = 0
		self.delay4 = 0
		self.pid = pid

	def setMaxDelay(self,maxDelay):
		self.maxDelay = maxDelay
	def setDelay1(self,Delay):
		self.delay1 = Delay
	def setDelay2(self,Delay):
		self.delay2 = Delay
	def setDelay3(self,Delay):
		self.delay3 = Delay
	def setDelay4(self,Delay):
		self.delay4 = Delay

	def getMaxDelay(self,):
		return self.maxDelay
	def getDelay1(self):
		return self.delay1 
	def setDelay2(self):
		return self.delay2
	def setDelay3(self):
		return self.delay3
	def setDelay4(self):
		return self.delay4
	def getPid(self):
		return self.pid
	
class DelayInfo(object):

	def __init__(self):
		self.delayCluster = {}
		self.subStreamNumber = 4
		self.maxDelay = []
		self.delay1 = []
		self.delay2 = [] 
		self.delay3 = [] 
		self.delay4 = [] 

	def parseFile(self,fileName,parseTime,subStreamId):

		readFile = open(fileName,'r')	
		for line in readFile:
			valueSet = line.split()
			if valueSet[0] == parseTime:
				valueSet = map(float,valueSet[4:9])
				self.delayInfo(valueSet)
				#print valueSet
		readFile.close()

		#print sum(self.maxDelay)/len(self.maxDelay)
		#print self.delay1
		#print self.delay2
		#print self.delay3
		#print self.delay4
		if subStreamId == -1:
			print self.standardDeviation(self.maxDelay)
			print self.standardDeviation(self.delay1)
			print self.standardDeviation(self.delay2)
			print self.standardDeviation(self.delay3)
			print self.standardDeviation(self.delay4)
		elif subStreamId == 0:
			print self.standardDeviation(self.maxDelay)
		elif subStreamId == 1:
			print self.standardDeviation(self.delay1)
		elif subStreamId == 2:
			print self.standardDeviation(self.delay2)
		elif subStreamId == 3:
			print self.standardDeviation(self.delay3)
		elif subStreamId == 4:
			print self.standardDeviation(self.delay4)
	def average(self,delay):
		return sum(delay)/len(delay)

	def variance(self,delay):
		averageDelay = self.average(delay)
		return map(lambda x: (x - averageDelay)**2,delay)	

	def standardDeviation(self,delay):
		varianceSet = self.variance(delay)
		return math.sqrt(self.average(varianceSet))

	def delayInfo(self,valueSet):
		self.maxDelay.append(valueSet[0])
		self.delay1 .append(valueSet[1])
		self.delay2 .append(valueSet[2])
		self.delay3 .append(valueSet[3])
		self.delay4 .append(valueSet[4])

	def setPeerDelayInfo(self,valueSet):

		pid = valueSet[1]	
		if self.delayCluster.has_key(pid):
			return
		else:
			peer = PeerDelay(pid)
			peer . setMaxDelay(valueSet[5])
			peer . setDelay1(valueSet[6])
			peer . setDelay2(valueSet[7])
			peer . setDelay3(valueSet[8])
			peer . setDelay4(valueSet[9])
			self.delayCluster[pid] = peer

if __name__ == '__main__':
	
	if len(sys.argv) == 3:
		fileName = sys.argv[1]
		parseTime = sys.argv[2]
		delayInfo = DelayInfo()
		delayInfo.parseFile(fileName,parseTime,-1)
	elif len(sys.argv) == 4:
		fileName = sys.argv[1]
		parseTime = sys.argv[2]
		delayInfo = DelayInfo()
		delayInfo.parseFile(fileName,parseTime,int(sys.argv[3]))
	else:
		print 'wrong command,should be python StandardDeviation.py client_data_of_chn_1.txt 1'


