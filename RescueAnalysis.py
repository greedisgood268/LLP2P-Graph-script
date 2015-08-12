import argparse
from Group import *

def getRescueStatusOverview():
	rescueTime = {}
	readFile = open('record_channel1.txt','r')
	for line in readFile:
		if 'CHNK_CMD_PEER_RESCUE,' in line:
			rescuePidHead = line.index(',pid:')	+ len(',pid:')
			rescuePidTail = line[rescuePidHead:].index(',manifest:')
			pid = int(line[rescuePidHead:rescuePidHead+rescuePidTail])
			if pid in rescueTime:
				rescueTime[pid] = rescueTime[pid] + 1
			else:
				rescueTime[pid] = 1 

	for key,value in sorted(rescueTime.iteritems(),key=lambda(k,v):(v,k)):
		print 'pid: %d, times: %d'% (key,value) 

def getPeerRescueParentAnalysis(pid):

	peerGroupInfo = getGroupPeers()
	rescueGroup = GroupTime()
	candidateSet = {}

	readFile = open('record_strategy1.txt','r')	
	for line in readFile:	

		if 'getRescueCandidateParentList,pid:' in line:
			rescuePeerHead = line.index('getRescueCandidateParentList,pid:') + len('getRescueCandidateParentList,pid:')		
			rescuePeerTail = rescuePeerHead + line[rescuePeerHead:].index(',rescueSubStreamId')
			rescuePeerPid = int(line[rescuePeerHead:rescuePeerTail])

			if rescuePeerPid != pid:
				continue

			if 'candidateRescueParent:' in line:
				head = line.index('candidateRescueParent:') + len('candidateRescueParent:')
				tail = head + line[head:].index(',appear')
				tempString = line[head:tail]
				candidatePid = int(tempString)
				try:
					if peerGroupInfo[rescuePeerPid] == peerGroupInfo[candidatePid]:
						rescueGroup.addSameTime()			
					else:
						rescueGroup.addDifferentTime()
				except:
					pass

				if candidatePid in candidateSet:
					candidateSet[candidatePid] = candidateSet[candidatePid] + 1
				else:
					candidateSet[candidatePid] = 1
	readFile.close()
	for key,value in sorted(candidateSet.iteritems(),key=lambda(k,v):(v,k)):
		print 'pid: %d, times: %d'% (key,value) 
	print rescueGroup.getResult()

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t',help='Input the analysis type.',choices=['Overview','peer'],type=str)
	parser.add_argument('-a',help='Input the peer Pid.',type=int)
	result = parser.parse_args()

	if result.t == 'Overview':
		getRescueStatusOverview()
	elif result.t == 'peer':		
		getPeerRescueParentAnalysis(result.a)
