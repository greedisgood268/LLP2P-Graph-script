import argparse

class Peer():

	def __init__(self,pid):
		self.pid = pid
		self.delay = []
		self.parentId = []

	def getPid(self):
		return self.pid

	def getParent(self,subStream):
		return int(self.parentId[subStream])	

	def setParent(self,parentId):
		self.parentId = parentId

	def setDelay(self,delay):
		self.delay = delay

	def getDelay(self,subStream):
		return float(self.delay[subStream])
		
def getTimeSlotInfo(timeSlot):

	peerInfo = {}
	readFile = open('client_data_of_chn_1.txt','r')
	for line in readFile:
		split = line.split()
		if len(split) != 19: 
			continue	
		if int(split[0]) == timeSlot:
			peer = Peer(int(split[1]))
			peer.setDelay(split[5:9])
			peer.setParent(split[15:])
			peerInfo[int(split[1])] = peer

	readFile.close()
	return peerInfo

def getAverageHopDelay(peerInfo):
	hopDelay = [0.0 for x in range(0,4)]
	times = [0 for x in range(0,4)]
	for item in peerInfo.values():	
		for index in range(0,4):	
			parentId = item.getParent(index)
			if parentId == 999999:
				hopDelay[index] = hopDelay[index] + item.getDelay(index)
				times[index] = times[index] + 1
			else:
				try:
					parent = peerInfo[parentId]	
					hopDelay[index] = hopDelay[index] - parent.getDelay(index) + item.getDelay(index)
					times[index] = times[index] + 1
				except KeyError:
					pass
				
	for index in range(0,4):
		if times[index] == 0:
			pass
		else:
			hopDelay[index] = hopDelay[index]/times[index]
	return hopDelay	

def getBoundHopDelay(peerInfo):

	maxHopDelay = [0.0 for x in range(0,4) ]
	minHopDelay = [0.0 for x in range(0,4) ]

	for item in peerInfo.values():	

		for index in range(0,4):	

			hopDelay = 0.0
			parentId = item.getParent(index)

			if parentId == 999999:
				hopDelay = item.getDelay(index)
			else:
				try:
					parent = peerInfo[parentId]	
					hopDelay = item.getDelay(index) - parent.getDelay(index) 
				except KeyError:
					continue	
			if hopDelay > maxHopDelay[index]:
				maxHopDelay[index] = hopDelay
			
			if hopDelay < minHopDelay[index]:
				minHopDelay[index] = hopDelay

	return maxHopDelay,minHopDelay	

def getOverallAverageHopDelay():

	readFile = open('client_data_of_chn_1.txt','r')
	overallAverageHopDelay = [0.0 for x in range(0,4)]
	times = [0.0 for x in range(0,4)]
	currentTime = -1 
	calculateSign = 0

	peerInfo = {}
	for line in readFile:

		split = line.split()
		if len(split) != 19: 
			continue	

		if (currentTime != int(split[0])) and (currentTime != -1) :
			peerDelay = getAverageHopDelay(peerInfo)		
			for index in range(0,4):
				overallAverageHopDelay[index] = overallAverageHopDelay[index] + peerDelay[index]
				times[index] = times[index] + 1
			peerInfo.clear()

		currentTime = int(split[0])
		peer = Peer(int(split[1]))
		peer.setDelay(split[5:9])
		peer.setParent(split[15:])
		peerInfo[int(split[1])] = peer
		
	peerDelay = getAverageHopDelay(peerInfo)		
	for index in range(0,4):
		overallAverageHopDelay[index] = overallAverageHopDelay[index] + peerDelay[index]
		times[index] = times[index] + 1

	readFile.close()

	for index in range (0,len(times)):
		overallAverageHopDelay[index] = overallAverageHopDelay[index]/times[index]
	return overallAverageHopDelay

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t',help='Give me the parse time',type=int,required = False)
	parser.add_argument('-a',help='Give me the hop delay type',choices=['average','bound','Overall'],type=str,required = True)
	result = parser.parse_args()
	
	if result.t != None:
		if result.a == 'average':
			peerInfo = getTimeSlotInfo(result.t)	
			hopDelayResult = getAverageHopDelay(peerInfo)
			print hopDelayResult

		elif result.a == 'bound':
			peerInfo = getTimeSlotInfo(result.t)	
			maxHop,minHop = getBoundHopDelay(peerInfo)
			print 'Max bound: ',maxHop
			print 'Min bound: ',minHop

	else:
		overallAverageHopDelay = getOverallAverageHopDelay()
		print overallAverageHopDelay
		


