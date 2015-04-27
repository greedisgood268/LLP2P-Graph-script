class PeerDelay(object):

	def __init__(self):

		self.times = []
		self.totalDelay = []

		for i in range(0,5):
			self.times.append(0.0)	
			self.totalDelay.append(0.0)

	def getAverageDelay(self,subStream):
		return self.totalDelay[subStream]/self.times[subStream]

	def setDelay(self,subStream,delay):
		self.times[subStream] += 1
		self.totalDelay[subStream] += delay

def parseFile(name):

	peerData = {}
	readFile = open(name,'r')
	for line in readFile:
		result = line.split()
		pid = int(result[1])
		if not (pid in peerData):
			peer = PeerDelay()
			peerData[pid] = peer

		for i in range(0,5):
			peerData[pid].setDelay(i,float(result[i+4]))
	
	keys = peerData.keys()
	for item in keys:
		print ("Pid:%d") % (item),
		for i in range(0,5):
			print ("%lf") % (peerData[item].getAverageDelay(i)),
		print '\n',
		
		
if __name__ == '__main__':
	parseFile('client_data_of_chn_1.txt')	
