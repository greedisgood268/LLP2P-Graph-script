import re
import sys
from AddressMapper import *

class PeerInTheSamePc(object): 

	def __init__(self):

		self.inTheSameComputer = 0		
		self.notInTheSameComputer = 0		
		self.counter = 0
		self.mapper = AddressMapper()

	def initData(self):

		self.inTheSameComputer = 0		
		self.notInTheSameComputer = 0		
		self.counter = 0
		self.mapper = AddressMapper()

	def parseCleanFile(self):

		self.initData()
		self.mapper.parseFile('content_strategy1.txt')

		fileName = 'parentTest.txt'
		readFile = open(fileName,'r')

		for line in readFile:
			self.__parseString(line)	

		readFile.close()
		print 'inTheSameComputer: ',self.inTheSameComputer,",notInTheSameComputer: ",self.notInTheSameComputer,",counter: " ,self.counter

	def __parseString(self,line):

		parentPidString = re.search(',parentPid:\s?[0-9]{1,9}',line)
		peerPidString = re.search(',pid:\s?[0-9]{1,9}',line)
		parentPid = re.findall('[0-9]{1,9}',parentPidString.group())
		pid = re.findall('[0-9]{1,9}',peerPidString.group())
		self.counter += 1
		if self.mapper.isPeerInTheSameComputer(parentPid[0],pid[0]):
			print line.strip()
			self.inTheSameComputer += 1		
		else:
			self.notInTheSameComputer += 1

	def parseFile(self,fileName):

		self.initData()
		self.mapper.parseFile('content_strategy1.txt')
		readFile = open(fileName,'r')

		for line in readFile:
			if "updatePeerCandidateParentInfo" in line:
				self.__parseString(line)
		readFile.close()
		print 'inTheSameComputer: ',self.inTheSameComputer,",notInTheSameComputer: ",self.notInTheSameComputer,",counter: " ,self.counter

if __name__ == '__main__':
	if len(sys.argv) == 2:	
		parser = PeerInTheSamePc()
		parser.parseFile(sys.argv[1])
	else:
		parser = PeerInTheSamePc()
		parser.parseCleanFile()
		



