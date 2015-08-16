import argparse
from HopDelay import *

nodeShape = ['polygon','ellipse','triangle','diamond','trapezium',\
			'parallelogram','hexagon','octagon','doublecircle',\
			'tripleoctagon','invtriangle','invtrapezium','circle','house',\
			'pentagon','septagon','octagon','doubleoctagon','tripleoctagon'\
			,'invhouse','Mdiamond','Msquare','Mcircle','rect','square'\
			,'star','note','folder','box3d','cds','rarrow','larrow']


originalWidth = 0.75
originalHeight= 0.5

class ChunkPeer():

	def __init__(self,pid):
		self.pid = pid
		self.parentPid = [ -1 for index in range(0,4)]
		self.groupId = [ -1 for index in range(0,4)]
		self.size = [ 0 for index in range(0,4)]
		self.normalChild = [ [] for index in range(0,4)]

	def addNormalChild(self,subStreamId,peer):
		self.normalChild[subStreamId].append(peer)

	def getAllNormalChild(self,subStreamId):
		return self.normalChild[subStreamId]

	def getPid(self):
		return self.pid

	def addSize(self,index):
		self.size[index] = self.size[index] + 1

	def getSize(self,index):
		return self.size[index]

	def setChunkParent(self,index,parentPid):
		self.parentPid[index] = parentPid

	def getChunkParent(self,index):
		return self.parentPid[index]

	def setGroupId(self,index,groupId):
		self.groupId[index] = groupId

	def getGroupId(self,index):
		return self.groupId[index]

class Peer():

	def __init__(self,pid):
		self.pid = pid
		self.normalChild = [ [] for index in range(0,4)]
		self.parentPid = [ 0 for index in range(0,4)]

	def getPid():
		return self.pid

	def addNormalChild(self,subStreamId,pid):
		self.normalChild[subStreamId].append(pid)

	def getAllNormalChild(self,subStreamId):
		return self.normalChild[subStreamId]

	def getTotalNumber(self,subStreamId):
		return len(self.normalChild[subStreamId])
	
	def setChunkParent(self,index,parentPid):
		self.parentPid[index] = parentPid

	def getChunkParent(self,index):
		return self.parentPid[index]

def getPeerList(time):
	peerList = {}
	readFile = open('client_data_of_chn_1.txt','r')
	for line in readFile:

		split = line.split()
		if len(split) != 19:
			continue
		if int(split[0]) > time:
			break;
		elif int(split[0]) != time:
			continue

		pid = int(split[1]) 
		if pid not in peerList:
			peer = Peer(pid)
			peerList[pid] = peer
		
		parentPid = map(int,split[15:]) 	

		for index in range(0,4):
			parent = parentPid[index]
			if parent in peerList:	
				parentPeer = peerList[parent]		
			else:
				parentPeer = Peer(parent)
				peerList[parent] = parentPeer
			parentPeer.addNormalChild(index,pid)
	readFile.close()
	return peerList

def parseChunkTreeList(chunkTree):

	for item in chunkTree.values():

		for index in range(0,4):

			parentPid = item.getChunkParent(index)
			if parentPid == -1:
				continue
			parentPeer = chunkTree[parentPid]
			parentPeer.addNormalChild(index,item)

	return chunkTree

def generateChunkTree(peerList):

	groupInfo = getGroupPeers()
	chunkList = {}

	for index in range(0,4):

		sameBranch = []
		differentBranch = [999999]
		chunkPid = -1 
		
		while len(differentBranch) > 0:

			chunkPid = chunkPid + 1
			peerId = differentBranch[0]	
			differentBranch.pop(0)
			targetPeer = peerList[peerId]

			if chunkPid in chunkList:	
				chunkPeer = chunkList[chunkPid]
			else:
				chunkPeer = ChunkPeer(chunkPid)
				chunkList[chunkPid] = chunkPeer

			chunkPeer.addSize(index)

			if peerId == 999999:
				groupId = -1 
			else:
				groupId = groupInfo[peerId]
				chunkPeer.setChunkParent(index,targetPeer.getChunkParent(index))

			chunkPeer.setGroupId(index,groupId)
			childBranch = targetPeer.getAllNormalChild(index)
			for item in childBranch:
				if groupInfo[item] == groupId:
					sameBranch.append(item)
					chunkPeer.addSize(index)
				else:
					differentBranch.append(item)
					treeChild = peerList[item]
					treeChild.setChunkParent(index,chunkPid)

			while len(sameBranch) > 0:
				sameBranchPeerPid = sameBranch[0]
				sameBranch.pop(0)
				sameBranchPeer = peerList[sameBranchPeerPid]	
				childSet = sameBranchPeer.getAllNormalChild(index)

				for childItem in childSet:
					if groupInfo[childItem] == groupId:
						sameBranch.append(childItem)
						chunkPeer.addSize(index)
					else:
						differentBranch.append(childItem)
						treeChild = peerList[childItem]
						treeChild.setChunkParent(index,chunkPid)

	return chunkList

def printGraph(topology):
	
	graph = 'digraph G {\n'
	groupToShape = [] 

	for item in topology.values():
		if item.getSize(0) > 0:

			if item.getGroupId(0) not in groupToShape:
				groupToShape.append(item.getGroupId(0))

			shapeIndex = groupToShape.index(item.getGroupId(0))
			graph = graph + str(item.getPid()) + '[shape=' + nodeShape[shapeIndex]			
			graph = graph +',fontsize='+str(14 *( 1+ item.getSize(0)/10))+\
					',fixedsize=True'+',width='+str(originalWidth *(1+item.getSize(0)/10))+\
					',height='+str(originalHeight*(1+item.getSize(0)/10))+'];\n'

	peerQueue = [topology[0]]
	while len(peerQueue) > 0:
		queuePeer = peerQueue[0]
		peerQueue.pop(0)
		child = queuePeer.getAllNormalChild(0)
		peerQueue = peerQueue + child
		for childPeer in child:
			graph = graph + str(queuePeer.getPid()) + '->' + str(childPeer.getPid()) + ';\n'

	graph = graph + '}'
	writeFile = open('output.txt','w')
	writeFile.write(graph)
	writeFile.close()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t',help='time',type=int,required=True)
	result = parser.parse_args()
	peerList = getPeerList(result.t)
	print 'yosh'
	chunkTree = generateChunkTree(peerList)
	print 'dosh'
	result = parseChunkTreeList(chunkTree)
	print 'kosh'
	
	printGraph(result)

