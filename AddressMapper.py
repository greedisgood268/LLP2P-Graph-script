import sys
import re

class Peer(object):
	def __init__(self,pid):
		self.pid = pid
		self.privateAddress = ''	
		self.publicAddress = ''	

	def setPublicAddress(self,publicAddress):
		self.publicAddress = publicAddress

	def setPrivateAddress(self,privateAddress):
		self.privateAddress = privateAddress

	def getPublicAddress(self):
		return self.publicAddress

	def getPrivateAddress(self):
		return self.publicAddress

class AddressMapper(object):

	def __init__(self):	
		self.peerCluster = {}
		self.inTheSameComputer = 1	
		self.notInTheSameComputer = 0	

	def isPeerInTheSameComputer(self,target ,peer):

		if self.peerCluster.has_key(target) and self.peerCluster.has_key(peer):
			targetPeer = self.peerCluster[target]
			currentPeer = self.peerCluster[peer]

			if (targetPeer.getPublicAddress() == currentPeer.getPublicAddress()) \
				and (targetPeer.getPrivateAddress() == currentPeer.getPrivateAddress()):
				return True 
			else:
				return False 
		else:
			return False 

	def hasAddressInfo(self,line):
		result = re.findall('\(.*\)',line) 
		if len(result) > 0:
			return True
		else:
			return False

	def checkAddressInfo(self,line):

		numberSet = re.findall('\d{1,9}',line)
		pid = numberSet[3]

		if self.peerCluster.has_key(pid):
			return
		else:
			addressInfo = re.findall('\([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\)',line)
			newPeer = Peer(pid)
			newPeer.setPublicAddress(addressInfo[0])
			newPeer.setPrivateAddress(addressInfo[1])
			self.peerCluster[pid] = newPeer
			
	def parseFile(self,fileName):
		readFile = open(fileName,'r')	
		for line in readFile:
			if(self.hasAddressInfo(line)):
				self.checkAddressInfo(line)
		readFile.close()

	def printContent(self):
		for key in self.peerCluster.keys():
			print key,self.peerCluster[key].getPublicAddress(), self.peerCluster[key].getPrivateAddress()

if __name__ == '__main__':

	mapper = AddressMapper()
	mapper.parseFile('content_strategy1.txt')
	mapper.printContent()	
