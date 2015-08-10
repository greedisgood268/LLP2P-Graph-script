class Peer():

	def __init__(self,pid):
		self.pid = pid
		self.time = 0

	def setTime(self):
		self.time = self.time + 1
	
	def getTime(self):
		return self.time

PeerList = {}

readFile = open('record_strategy1.txt','r')
for line in readFile:
	if 'candidateJoinParent:' in line:
		head = line.index('candidateJoinParent:')+len('candidateJoinParent:')
		tail = head + line[head:].index(',')
		tempString = line[head:tail]

		if PeerList.has_key(int(tempString)):
			peer = PeerList[int(tempString)]
		else:
			peer = Peer(int(tempString))

		peer.setTime()
		PeerList[int(tempString)] = peer

	elif 'candidateRescueParent:' in line:
		head = line.index('candidateRescueParent:')+len('candidateRescueParent:')
		tail = head + line[head:].index(',')
		tempString = line[head:tail]

		if PeerList.has_key(int(tempString)):
			peer = PeerList[int(tempString)]
		else:
			peer = Peer(int(tempString))

		peer.setTime()
		PeerList[int(tempString)] = peer

	elif ('requestPeerToMove' in line) and ('parentPeerPid' in line):
		head = line.index('parentPeerPid:') + len('parentPeerPid:')
		tail = head + line[head:].index(',subStreamId')
		tempString = line[head:tail]

		if PeerList.has_key(int(tempString)):
			peer = PeerList[int(tempString)]
		else:
			peer = Peer(int(tempString))

		peer.setTime()
		PeerList[int(tempString)] = peer

readFile.close()
values = PeerList.values()
result = sorted(values, key=lambda Peer: Peer.time ,reverse= True)
for item in result:
	print item.getTime() 
