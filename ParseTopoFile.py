import re
import sys
from ParseFile import *

class ParseTopoFileByTime(ParseFileByTime):

	def __init__(self):
		super(ParseTopoFileByTime,self).__init__()
		self.topoMatch = re.compile('\(.*\)')
		self.startOfMergeStatement = 0
		self.endOfMergeStatement = -1 
		self.notStartOfMergeStatement = 1
		self.notEndOfMergeStatement = 2
		self.contentSubStreamStatement = 'sub stream id :' 
		self.notOfSubStreamStatement = 1
		self.ofSubStreamStatement = 0
		self.isOfTopoStatement = 0
		self.isNotOfTopoStatement = 1
		self.ERROR = -1

	def isNewMergeStatement(self,line): 
		if re.search('mergeOperation starts',line) != None:
			return self.startOfMergeStatement
		else:
			return self.notStartOfMergeStatement

	def isEndOfMergeStatement(self,line): 
		if re.search('mergeOperation ends',line) != None:
			return self.endOfMergeStatement
		else:
			return self.notEndOfMergeStatement

	def getSubStreamId(self,line):
		streamLine = re.search("sub stream id :.*",line)
		result = self.numberMatch.search(streamLine.group(0))
		return int(result.group())

	def isOfSubStreamStatement(self,line):

		if(re.search('sub stream id :',line)) != None:
			return self.ofSubStreamStatement 
		else: 
			return self.notOfSubStreamStatement 

	def printSubStream(self,readFile,subStreamId):

		writeFile = open(str(self.startTime[0])+'-'+str(self.startTime[1])+'-topo'+str(subStreamId)+'.txt','w')
		line = readFile.readline()
		line = readFile.readline()
		while self.isTopoStatement(line) == self.isOfTopoStatement:
			writeFile.write(line)
			line = readFile.readline()
		writeFile.close()
		return line

	def isTopoStatement(self,line):
		if self.topoMatch.search(line) != None:	
			return self.isOfTopoStatement
		else:
			return self.isNotOfTopoStatement

	def parseFile(self):
	
		readFile = open(self.inputFileName,'r')

		while True:
			line = readFile.readline()
			if line == '':
				break

			if self.isTimeInThePeriod( self.getLineTime(line) ) == self.correctTime and self.isNewMergeStatement(line) == self.startOfMergeStatement:
				line = readFile.readline()
				while self.isOfSubStreamStatement(line) == self.ofSubStreamStatement:
					subStreamId = self.getSubStreamId(line)
					line = self.printSubStream(readFile, subStreamId)
				break
		readFile.close()

def getTime(line):
	return map(int,line.split('-'))	


if __name__ == '__main__':
	# inputFileName startTime durationTime	

	test = ParseTopoFileByTime();
	startTime = getTime(sys.argv[2])
	durationTime = getTime(sys.argv[3])

	test.setInputFile(sys.argv[1]);

	test.setStartTime(startTime[0],startTime[1])
	test.setDurationTime(durationTime[0],durationTime[1])

	test.parseFile()
