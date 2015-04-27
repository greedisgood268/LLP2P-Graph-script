import re
import sys

class ParseFileByTime(object):
	
	def __init__(self):
		
		self.numberMatch = re.compile('\d{1,9}')
		self.matchTimeQuantum = re.compile('\[.*\]')
		self.correctTime = 1
		self.incorrectTime = -1

		self.startTime = [] 
		self.endTime = []

		self.inputFileName = ''
		self.outputFileName = ''

	def setStartTime(self,minute,second):

		self.startTime.append(minute)
		self.startTime.append(second)
		self.startTime.append(0)  

	def setDurationTime(self, durationMinute, durationSecond):

		spareMinute = 0
		self.endTime.append(0)
		self.endTime.append(0)
		self.endTime.append(0)

		if durationSecond + self.startTime[1] > 60:
			spareMinute = durationSecond + self.startTime[1] / 60
			self.endTime[1] = durationSecond + self.startTime[1] - spareMinute*60 
		else:
			self.endTime[1] = durationSecond + self.startTime[1]

		if spareMinute != 0:
			self.endTime[0] = self.startTime[0] + durationMinute + spareMinute 
		else:
			self.endTime[0] = self.startTime[0] + durationMinute
	

	def setInputFile(self, inputFileName):
		self.inputFileName = inputFileName

	def setOutputFile(self, outputFileName):
		self.outputFileName = outputFileName 

	def getLineTime(self, line):
		timeList = self.matchTimeQuantum.findall(line)
		if timeList == None:
			print 'Failed to find a time'
			return
		
		timeDuration = timeList[0] 
		timeSplit = self.numberMatch.findall(timeDuration)	
		return map(int,timeSplit)

	def isTimeLargerThanStartTime(self,timeList):

		if timeList == None:	
			return self.incorrectTime

		if timeList[0] < self.startTime[0]:
			return self.incorrectTime
		if timeList[0] == self.startTime[0]: 
			if timeList[1] >= self.startTime[1]:   
				return self.correctTime
			else:
				return self.incorrectTime
		else:
			return self.correctTime

	def isTimeSmallerThanStopTime(self,timeList):

		if timeList == None:	
			return self.incorrectTime
		
		if timeList[0] < self.endTime[0]:
			return self.correctTime
		elif timeList[0] == self.endTime[0]: 
			if timeList[1] < self.endTime[1]:   
				return self.correctTime
			elif timeList[1] == self.endTime[1] and timeList[2] <= self.endTime[2]:
				return self.correctTime
			else:
				return self.incorrectTime
		else:
			return self.incorrectTime

	def isTimeInThePeriod(self,timeList):	
		
		if self.isTimeSmallerThanStopTime(timeList) == self.correctTime and self.isTimeLargerThanStartTime(timeList) == self.correctTime:
			return self.correctTime	
		else:
			return self.incorrectTime

	def parseFile(self):
	
		readFile = open(self.inputFileName,'r')
		writeFile = open(self.outputFileName,'w')

		for line in readFile:
			if self.isTimeInThePeriod( self.getLineTime(line) ) == self.correctTime:
				writeFile.write(line)

def getTime(line):
	return map(int,line.split('-'))	


if __name__ == '__main__':
	# inputFileName startTime durationTime	

	test = ParseFileByTime();
	startTime = getTime(sys.argv[2])
	durationTime = getTime(sys.argv[3])

	test.setInputFile(sys.argv[1]);
	test.setOutputFile(sys.argv[2]+"-"+sys.argv[1]);

	test.setStartTime(startTime[0],startTime[1])
	test.setDurationTime(durationTime[0],durationTime[1])

	test.parseFile()
