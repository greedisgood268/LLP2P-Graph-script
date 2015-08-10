fileName = 'client_data_of_chn_1.txt'

class PeerDelay():

	def __init__(self,pid):
		self.pid = pid
		self.delay = {}	
		self.times = 0
		self.clock = 0

		for index in range(0,5):
			self.delay[index] = 0.0


	def setDelay(self,delay,clock):
		for index in range(0,5):
			self.delay[index] = self.delay[index] + float(delay[index])
		self.times = self.times + 1
		self.clock = clock

	def getDelay(self):
		return self.delay

	def getAverageDelay(self):
		for index in range(0,5):
			self.delay[index] = self.delay[index] / self.times
		return (self.clock, self.delay)

	def getPid(self):
		return self.pid

def parseFile():

	readFile = open(fileName,'r')
	peerList = {}
	lastIndex = 0
	for line in readFile:
		arrayItem = line.split()		
		if int(arrayItem[1]) in peerList:	
			peer = peerList[int(arrayItem[1])]
		else:
			peer = PeerDelay(int(arrayItem[1])) 
			peerList[int(arrayItem[1])] = peer

		peer.setDelay(arrayItem[4:9],int(arrayItem[0]))
		peerList[int(arrayItem[1])] = peer
		lastIndex = int(arrayItem[0])
	readFile.close()
	return lastIndex,peerList

if __name__ == '__main__':

	lastIndex,peerList = parseFile()	
	delay = [0.0 for index in range(0,5)]
	number = 0

	for item in peerList.values():

		delayItem = item.getAverageDelay()
		if delayItem[0] < lastIndex - 1:
			continue
		for index in range(0,5):
			delay[index] = delay[index]+ (delayItem[1])[index] 
			
		number = number + 1

	for index in range(0,5):
		delay[index] =  delay[index] / number

	print delay	



