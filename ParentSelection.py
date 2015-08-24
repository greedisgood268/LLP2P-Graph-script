from Group import RTTGroup

class GroupTime():
	
	def __init__(self):

		self.sameTime = 0
		self.differentTime = 0
		self.totalTime = 0.0

	def addSameTime(self):
		self.sameTime = self.sameTime + 1
		self.totalTime = self.totalTime + 1

	def addDifferentTime(self):
		self.differentTime = self.differentTime + 1
		self.totalTime = self.totalTime + 1
	
	def getResult(self):
		if self.totalTime == 0.0:
			return 'Same Group: '+ '{:d}'.format(self.sameTime)+',Different Time: ' + '{:d}'.format(self.differentTime)+\
			',Same Group Ratio: '+'{:f}'.format(0)
		else:
			return 'Same Group: '+ '{:d}'.format(self.sameTime)+',Different Time: ' + '{:d}'.format(self.differentTime)+\
			',Same Group Ratio: '+'{:f}'.format(self.sameTime/self.totalTime)

def sameGroup():

	Group = RTTGroup()
	pidGroupPair = Group.getGroupInfo()
	moveTime = GroupTime()
	rescueTime = GroupTime()
	joinTime = GroupTime()

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
					joinTime.addSameTime()
				else:
					joinTime.addDifferentTime()
			except:
				pass

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
					rescueTime.addSameTime()			
				else:
					rescueTime.addDifferentTime()
			except:
				pass

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
					moveTime.addSameTime()
				else:
					moveTime.addDifferentTime()
			except:
				pass

	readFile.close()	

	print 'Join,' + joinTime.getResult()
	print 'Rescue,' + rescueTime.getResult()
	print 'Move,' + moveTime.getResult()

if __name__ == '__main__':
	sameGroup()
