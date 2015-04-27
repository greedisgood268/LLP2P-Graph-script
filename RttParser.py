import sys
import os

def drawGraph(time,fileSet):

	files = " "
	value =  files.join(fileSet)
	command0 = "./topo "	 + "GROUP " + time +"-topo0.txt "+time+"-group0.jpeg "+ value 
	os.system(command0)	
	command1 = "./topo "	 + "GROUP " + time +"-topo1.txt "+time+"-group1.jpeg "+ value 
	os.system(command1)	
	command2 = "./topo "	 + "GROUP " + time +"-topo2.txt "+time+"-group2.jpeg "+ value 
	os.system(command2)	
	command3 = "./topo "	 + "GROUP " + time +"-topo3.txt "+time+"-group3.jpeg "+ value 
	os.system(command3)	

if __name__ == '__main__':

	fileSet = []

	rttFile = open(sys.argv[1],'r')	
	for line in rttFile:

		if "printInfo,groupId:" in line: 

			temporyLine = 'printInfo,groupId:'
			target = line[line.index("printInfo,groupId:") + len(temporyLine):]	
			nameSplit = target.split(",")
			fileName = 'hight' + nameSplit[0].strip() +'.txt'
			pidSet = target[target.index("pid:") + 4:].strip().split(",")
			writeFile = open(fileName,'w')

			for value in pidSet:
				if value is '':
					break
				writeFile.write(value+'\n')
			writeFile.close()

			fileSet.append(fileName)

	rttFile.close()
	drawGraph(sys.argv[2],fileSet)

