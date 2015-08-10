class Peer():

	def __init__(self,pid):
		self.pid = pid
		self.time = 0

	def setTime(self):
		self.time = self.time + 1
	
	def getTime(self):
		return self.time


def getGroupPeers():
	
	readFile = open('record_RttManager1.txt','r')
	GroupList = {}

	for line in readFile:

		if 'printInfo begin,group size:' in line:	
			GroupList.clear()

		if 'printInfo,groupId:' in line:
			groupIdHead = line.index('printInfo,groupId:') + len('printInfo,groupId:')
			groupIdTail = line.index(',pid:')
			groupId = int(line[groupIdHead: groupIdTail])
			pidSet = line[groupIdTail+len(',pid:'):].strip().split(',')
			pidSet = map(int,filter(None,pidSet))
			for item in pidSet:
				GroupList[item] = groupId
	'''			
	for item in GroupList.items():
		print item[0],",",item[1]
	'''
	readFile.close()
	return GroupList

def sameGroup(pidGroupPair):
	times = 0
	sametimes = 0

	readFile = open('record_strategy1.txt','r')
	for line in readFile:
		if 'candidateJoinParent:' in line:
			head = line.index('candidateJoinParent:')+len('candidateJoinParent:')
			tail = head + line[head:].index(',')
			tempString = line[head:tail]
			candidatePid = int(tempString)

			pidHead = line.index(',pid:')+len(',pid:')
			pidTail = pidHead + line[pidHead:].index(',')
			pid = int(line[pidHead:pidTail])
			try:
				if pidGroupPair[pid] == pidGroupPair[candidatePid]:
					sametimes = sametimes + 1
			except:
				pass

			times = times + 1

		elif 'candidateRescueParent:' in line:
			head = line.index('candidateRescueParent:')+len('candidateRescueParent:')
			tail = head + line[head:].index(',')
			tempString = line[head:tail]

			candidatePid = int(tempString)

			pidHead = line.index(',pid:')+len(',pid:')
			pidTail = pidHead + line[pidHead:].index(',')
			pid = int(line[pidHead:pidTail])
			try:
				if pidGroupPair[pid] == pidGroupPair[candidatePid]:
					sametimes = sametimes + 1
			except:
				pass
			times = times + 1

		elif ('requestPeerToMove' in line) and ('parentPeerPid' in line):
			head = line.index('parentPeerPid:') + len('parentPeerPid:')
			tail = head + line[head:].index(',subStreamId')
			tempString = line[head:tail]

			candidatePid = int(tempString)

			pidHead = line.index('pid:')+len('pid:')
			pidTail = pidHead + line[pidHead:].index(',')
			pid = int(line[pidHead:pidTail])
			try:
				if pidGroupPair[pid] == pidGroupPair[candidatePid]:
					sametimes = sametimes + 1
			except:
				pass
			times = times + 1

	readFile.close()	
	print (sametimes/float(times))

if __name__ == '__main__':
	pidGroupPair = getGroupPeers()
	sameGroup(pidGroupPair)
