import argparse
import os
from HopDelay import *
from Group import GeoGroup,RTTGroup

nodeScale = 10
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

	def removeNormalChild(self,subStreamId,removePeer):
		for peer in self.normalChild[subStreamId]:
			if peer.getPid() == removePeer.getPid():
				self.normalChild[subStreamId].remove(peer)
				break

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
			if parentPid[index] in peerList:	
				parentPeer = peerList[parentPid[index]]		
			else:
				parentPeer = Peer(parentPid[index])
				peerList[parentPid[index]] = parentPeer
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

def printChunkTree(chunkTree):
	
	for index in range(0,4):
		print 'subStreamId:',index
		for peer in chunkTree.values():
			print 'pid:',peer.getPid(),'childPid:',
			for child in peer.getAllNormalChild(index):
				print child.getPid(), 
			print '\n',

def generateChunkTreeDFS(peerList,groupType='RTT'):

	if groupType == 'RTT':
		rttGroup = RTTGroup()	
		groupInfo = rttGroup.getGroupInfo()
	else:
		geoGroup = GeoGroup()
		groupInfo = geoGroup.getGroupInfo(duration=50)

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

def getFloatRatio(number):
	value = number/nodeScale + (number%float(nodeScale))/10
	return value 

def printGraph(topology,subStreamId=0,outputName='haha.jpeg'):
	
	graph = 'digraph G {\n'
	groupToShape = [] 

	for item in topology.values():
		if item.getSize(subStreamId) > 0:

			if item.getGroupId(subStreamId) not in groupToShape:
				groupToShape.append(item.getGroupId(subStreamId))

			shapeIndex = groupToShape.index(item.getGroupId(subStreamId))
			graph = graph + str(item.getPid()) + '[shape=' + nodeShape[shapeIndex]			
			graph = graph +',fontsize='+\
					str(14 *( 1+ getFloatRatio(item.getSize(subStreamId))))+\
					',fixedsize=True'+',width='+str(originalWidth *(1+getFloatRatio(item.getSize(subStreamId))))+\
					',height='+str(originalHeight*(1+getFloatRatio(item.getSize(subStreamId))))+'];\n'
			print 'Pid:',item.getPid(),',groupId:',item.getGroupId(subStreamId)

	peerQueue = [topology[0]]
	while len(peerQueue) > 0:
		queuePeer = peerQueue[0]
		peerQueue.pop(0)
		child = queuePeer.getAllNormalChild(subStreamId)
		peerQueue = peerQueue + child
		for childPeer in child:
			graph = graph + str(queuePeer.getPid()) + '->' + str(childPeer.getPid()) + ';\n'

	graph = graph + '}'
	writeFile = open('output.txt','w')
	writeFile.write(graph)
	writeFile.close()
	os.system('dot output.txt -T jpeg -o '+outputName)

def splitPeersIntoGroups(subStreamId,peers):
	
	peersGroup = []
	idSet = []

	for peer in peers:

		if peer.getGroupId(subStreamId) not in idSet:	
			idSet.append(peer.getGroupId(subStreamId))
			group = [peer]
			peersGroup.append(group)
		else:
			peersGroup[idSet.index(peer.getGroupId(subStreamId))].append(peer)

	return peersGroup

def changePeerToANewParent(peers,parentId,subStreamId):

	for peer in peers:
		peer.setChunkParent(subStreamId,parentId)

def simplified(subStreamId,chunkTree):
	
	processQueue = [chunkTree[0]]
	while len(processQueue) > 0:
		peer = processQueue.pop(0)
		child = peer.getAllNormalChild(subStreamId)
		peerGroups = splitPeersIntoGroups(subStreamId,child)
		
		for group in peerGroups:

			if len(group) == 1:
				continue

			head = group[0]
			for member in group:
				if member.getPid() == head.getPid():
					continue
				children = member.getAllNormalChild(subStreamId)	
				addChildren(subStreamId,head,children)	
				chunkTree.pop(member.getPid())
				peer.removeNormalChild(subStreamId,member)

			for value in range(0,len(group)-1):
				head.addSize(subStreamId)

		processQueue = processQueue + peer.getAllNormalChild(subStreamId)

def addChildren(subStreamId,peer,child):
	for item in child:
		peer.addNormalChild(subStreamId,item)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t',help='Parse time',type=int,required=True)
	parser.add_argument('-l',help='Group type',choices=['RTT','GEO'],default='RTT',type=str)
	parser.add_argument('-a',help='Graph type',choices=['DFS','Simplified'],type=str,required=True)
	parser.add_argument('-o',help='Graph name',type=str,default='haha.jpeg')
	parser.add_argument('-k',help='SubStreamId',type=int,required=True)

	parseResult = parser.parse_args()
	peerList = getPeerList(parseResult.t)
	chunkTree = generateChunkTreeDFS(peerList,groupType=parseResult.l)

	parseChunkTreeList(chunkTree)


	if parseResult.a != 'DFS':
		simplified(parseResult.k,chunkTree)

	printGraph(chunkTree,subStreamId=parseResult.k,outputName=parseResult.o)


