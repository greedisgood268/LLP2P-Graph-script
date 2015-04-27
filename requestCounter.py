import sys

class peer:

	def __init__(self,pid):
		self.pid = pid;
		self.occurrence = 0
	def getPid(self):
		return self.pid

	def addOccurrence(self):
		self.occurrence += 1

	def getOccurrence(self):
		return self.occurrence
		
def parseFile(fileName,printType):
	peerList={}
	readFile = open(fileName,'r')	
	for line in readFile:
		line = line.replace('\n','')
		if line in peerList:
			peerList[line].addOccurrence() 
		else:
			peerList[line] = peer(line)
			peerList[line].addOccurrence()

	readFile.close()

	valueList = peerList.values()
	valueList = sorted(valueList,key = lambda peer: peer.occurrence, reverse = True)

	for data in valueList:
		if printType == 1:
			print data.getPid(),",",data.getOccurrence()
		else:
			print data.getPid()

if __name__ == '__main__':
	if len(sys.argv) > 2:
		parseFile(sys.argv[1],1)
	else:
		parseFile(sys.argv[1],0)
