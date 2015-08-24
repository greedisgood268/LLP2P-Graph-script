from geoip import geolite2

class Group(object):

	def __init__(self):	
		self.GroupList = {}	

	def isInTheSameGroup(self,pidA,pidB):
		try:
			return self.GroupList[pidA] == self.GroupList[pidB]
		except KeyError:
			print pidA,pidB,'are not shown in the group information' 
			return False

class GeoGroup(Group):
	
	def getGroupInfo(self,fileName = 'client_data_of_chn_1.txt',time=200,duration=100,classifyType = 'continent'):
		
		print 'We get the Geographical Group Info from:',fileName,',from time slot:',time,\
			',with duration:',duration,',and classifyType:',classifyType
		self.GroupList = {}
		readFile = open(fileName,'r')

		for line in readFile:

			split = line.split()			
			if len(split) != 19:
				continue

			if int(split[0]) < time:
				continue
			elif int(split[0]) > (time + duration):
				break

			match = geolite2.lookup(split[2])

			if classifyType == 'continent':
				value = match.continent
			elif classifyType == 'country':
				value = match.country

			self.GroupList[int(split[1])] = value 

		readFile.close()
		return self.GroupList

class RTTGroup(Group):

	def getGroupInfo(self,fileName = 'record_RttManager1.txt'):
		print 'We get the RTT Group Info from',fileName
		self.GroupList = {}
		readFile = open(fileName,'r')

		for line in readFile:

			if 'printInfo,groupId:' in line:
				groupIdHead = line.index('printInfo,groupId:') + len('printInfo,groupId:')
				groupIdTail = line.index(',pid:')
				groupId = int(line[groupIdHead: groupIdTail])
				pidSet = line[groupIdTail+len(',pid:'):].strip().split(',')
				pidSet = map(int,filter(None,pidSet))
				for item in pidSet:
					self.GroupList[item] = groupId

		readFile.close()
		return self.GroupList

class Branch(object):

	def __init__ (self):
		self.sameBranch = 0.0
		self.differentBranch = 0.0
		self.totalBranch = 0.0
		self.counter = 0.0

	def getCounter(self):
		return self.counter

	def addCounter(self,counter):
		self.counter = self.counter + counter

	def addSameGroupBranch(self,branch):
		self.sameBranch = self.sameBranch + branch
		self.totalBranch = self.totalBranch + branch

	def addDifferentGroupBranch(self,branch):
		self.differentBranch = self.differentBranch + branch
		self.totalBranch = self.totalBranch + branch

	def getSameGroupBranchRate(self):
		return self.sameBranch/self.totalBranch

	def getDifferentBranchRate(self):
		return self.differentBranch/self.totalBranch
	
	def getSameGroupBranchNumber(self):
		return self.sameBranch, self.totalBranch

	def getDifferentBranchRate(self):
		return self.differentBranch,self.totalBranch

