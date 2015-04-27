import re
import os

startStatementFlag = 0
subStreamPatternFlag = 1
endOfStatementFlag = 2
noneFlag = 4
topoFlag = 5

startOfStatementPattern = re.compile('mergeOperation starts')
subStreamPattern = re.compile('sub stream id\s')
endOfStatementPattern = re.compile('Total peer')
topoPattern = re.compile('\(.*\)')
timePattern = re.compile('\d{1,9}')
subStreamIdPattern = re.compile('\d')
position = 0
readFileName = 'content_strategy1.txt'
targetFile = open(readFileName,'r')

position = 0 
targetFile.seek(position)
writeFile = ''	

def getTime(line):
	respond = ''
	index = 0
	for a in range(0,4):

		result = timePattern.search(line,index)	
		if result:
			if len(respond):
				respond = respond + '-' + result.group() 
			else:
				respond = result.group()

			index = result.end()
		else:
			break
		
	return respond

def getSubStreamId(targetLine):
	line = subStreamPattern.search(targetLine)
	if line :
		tempLine = subStreamIdPattern.search(targetLine,line.end())	
		if tempLine :
			return int(tempLine.group())
		else:
			return -1
	else:	
		return -1

def printTopologyToTargetFile(readFile, targetFile):
	
	while True:
		line = readFile.readline()
		if not line:
			break
		if checkLineType(line) == topoFlag:
			targetFile.write(line)
		else:
			return line

def checkLineType(line):

	if startOfStatementPattern.search(line):
		return startStatementFlag	
	elif subStreamPattern.search(line):
		return subStreamPatternFlag
	elif endOfStatementPattern.search(line): 
		return endOfStatementFlag
	elif topoPattern.search(line):
		return topoFlag
	else:
		return noneFlag
		
def getNextStatement(targetFile):
	
	while True:
		line = targetFile.readline()
		if not line:
			return line	
		if checkLineType(line)  == startStatementFlag:
			return line	

def parserSubStream(targetFile,timeLine):

	line = targetFile.readline()

	for a in range(0,4):
		
		subStreamId = getSubStreamId(line)
		if subStreamId == -1:
			return

		line = targetFile.readline()
		writeFileName = getTime(timeLine) + '-' + str(subStreamId) + '.txt'
		writegraphName = getTime(timeLine) + '-' + str(subStreamId) + '.jpeg'
		writeFile = open(writeFileName,'w')	
		line = printTopologyToTargetFile(targetFile,writeFile)
		writeFile.close()
		deleteCommand = 'rm ' + writeFileName
		command = './topo ' + writeFileName +' '+ writegraphName 
		os.system(command)
		os.system(deleteCommand)


while True:

	line = targetFile.readline()

	if line:
		respond = getNextStatement(targetFile)		
		if respond:
			parserSubStream(targetFile,respond)
		else:
			break
	else:
		break	


