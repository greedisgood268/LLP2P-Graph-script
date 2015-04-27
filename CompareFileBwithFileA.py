import sys
class Target:

	def __init__(self):

		self.foundList= {}	

	def parseFile(self,targetFile):

		readFile = open(targetFile,'r')	
		for line in readFile:
			line = int(line.strip('\n'))
			if self.foundList.has_key(line):
				self.foundList[line] += 1
			else:
				self.foundList[line] = 1
		readFile.close()

	def startToCompareFiles(self,targetFile):

		writeFile = open('compareResult.txt','w')	
		readFile = open(targetFile)
		duplicatedItem = []
		nonDuplicatedItem = []

		for line in readFile:
			line = int(line.strip('\n'))
			if self.foundList.has_key(line):
				duplicatedItem.append(line)
			else:
				nonDuplicatedItem.append(line)
		readFile.close()
		
		duplicatedSet = list(set(duplicatedItem))
		nonDuplicatedSet = list(set(nonDuplicatedItem))

		duplicatedSet = sorted(duplicatedSet)
		nonDuplicatedSet = sorted(nonDuplicatedSet)

		writeFile.write("*******duplicated Item*******\n")
		for data in duplicatedSet:
			writeFile.write(str(data)+"\n")

		writeFile.write("*******nonDuplicated Item*******\n")
		for data in nonDuplicatedSet:
			writeFile.write(str(data)+"\n")
		writeFile.close()

if __name__=='__main__':
	parser = Target()
	parser.parseFile(sys.argv[1])
	parser.startToCompareFiles(sys.argv[2])
	

