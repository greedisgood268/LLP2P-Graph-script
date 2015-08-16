class Peer():

	def __init__(self,pid):
		self.pid = pid
		self.child = [ [] for index in range(0,4)]

	def getAllTheChild(self,subStream):
		return self.child[subStream]
	
	def addChild(self,subStream,pid):
		self.child[subStream].append(pid)

class Hop():

	def __init__(self):

		self.time = 0
		self.length = 0

	def getTime(self):
		return self.time

	def addLength(self,depth,time):
		self.time = self.time + time
		self.length = self.length + (time * depth) 

	def getLength(self):
		return self.length

	def getAverageHopLength(self):
		if	self.time == 0:
			return 0
		return self.length/float(self.time)

def calculateHop():

	readFile = open('client_data_of_chn_1.txt','r')
	processTime = -1 
	peerList = {}
	hopArray = [ Hop() for x in range(0,4)]

	for line in readFile:

		split = line.split()	
		if len(split) != 19:	
			continue

		if (processTime != int(split[0])) and (processTime != -1):
			
			for index in range(0,4):

				depth = 0
				processArray = peerList[999999].getAllTheChild(index)
				levelArray = []

				while len(processArray) > 0:

					depth = depth + 1 
					hopArray[index].addLength( depth ,len(processArray) ) 
					for item in processArray:
						if item in peerList:
							targetPeer = peerList[item]
							levelArray = levelArray + targetPeer.getAllTheChild(index)

					processArray = levelArray
					levelArray = []

			peerList.clear()
			for index in range(0,4):
				print hopArray[index].getAverageHopLength(),
				hopArray[index] = Hop()
			print '\n',
		processTime = int(split[0])
		pid = int(split[1])

		for index in range(0,4):
			subStreamParent = int(split[15+index])
			if subStreamParent not in peerList:
				peerList[subStreamParent] = Peer(subStreamParent)
			peerList[subStreamParent].addChild(index,pid)

	readFile.close()

if __name__ == '__main__':
	calculateHop()




