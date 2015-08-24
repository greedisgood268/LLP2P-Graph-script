from Group import *
import argparse

def timeSlotCalculation( timeGroupBranch, overallGroupBranch):

	for index in range(0,4):
		sameGroupBranch, totalNumber = timeGroupBranch[index].getSameGroupBranchNumber()
		overallGroupBranch[index].addSameGroupBranch(sameGroupBranch)
		overallGroupBranch[index].addCounter(totalNumber)

def getOverallBranchAccuracy(classifyType,accuracy,fileName='client_data_of_chn_1.txt'):
	
	rttGroup = RTTGroup() 
	rttGroup.getGroupInfo()

	geoGroup = GeoGroup() 
	geoGroup.getGroupInfo(time=50,classifyType=classifyType)

	timeGroupBranch = [Branch() for x in range(0,4)]
	overallGroupBranch = [Branch() for x in range(0,4)]
	currentTime = -1

	readFile = open(fileName,'r')
	for line in readFile:

		split = line.split()
		if len(split) != 19:
			continue

		if (currentTime != -1) and (int(split[0]) != currentTime):
			timeSlotCalculation( timeGroupBranch, overallGroupBranch)

		currentTime = int(split[0])
		pid = int(split[1]) 
		parents = map(int,split[15:])

		if accuracy == 'sameGroup':
			for index in range(0,4):	
				if parents[index] == 999999:
					pass
					#timeGroupBranch[index].addDifferentGroupBranch(1)
				elif rttGroup.isInTheSameGroup(pid,parents[index]) and geoGroup.isInTheSameGroup(pid,parents[index]):
					timeGroupBranch[index].addSameGroupBranch(1)
				else:
					timeGroupBranch[index].addDifferentGroupBranch(1)
		else:
			for index in range(0,4):	
				if parents[index] == 999999:
					pass
					#timeGroupBranch[index].addDifferentGroupBranch(1)
				elif rttGroup.isInTheSameGroup(pid,parents[index]) and geoGroup.isInTheSameGroup(pid,parents[index]):
					timeGroupBranch[index].addSameGroupBranch(1)
				elif (rttGroup.isInTheSameGroup(pid,parents[index]) == False) and (geoGroup.isInTheSameGroup(pid,parents[index]) == False):
					timeGroupBranch[index].addSameGroupBranch(1)
				else:
					timeGroupBranch[index].addDifferentGroupBranch(1)

	timeSlotCalculation( timeGroupBranch, overallGroupBranch)
	readFile.close()
	return overallGroupBranch

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t',help='Input the Geographical accuracy.',choices=['continent','country'],type=str,default='continent')
	parser.add_argument('-a',help='Input the accuracy type.',choices=['sameGroup','accuracy'],type=str,default='sameGroup')
	parseResult = parser.parse_args()

	result = getOverallBranchAccuracy(classifyType=parseResult.t,accuracy=parseResult.a)

	if parseResult.a == 'sameGroup':
		for index in range(0,4):
			sameGroupBranch,totalNumber = result[index].getSameGroupBranchNumber()		
			counter = result[index].getCounter()
			print 'subStreamId:',index, ',sameGroupBranch:',sameGroupBranch,',differentGroupBranch:',counter - sameGroupBranch,\
					',sameGroupRatio:', sameGroupBranch/counter
	else:
		for index in range(0,4):
			sameGroupBranch,totalNumber = result[index].getSameGroupBranchNumber()		
			counter = result[index].getCounter()
			print 'subStreamId:',index, ',correct:',sameGroupBranch,',incorrect:',counter - sameGroupBranch,\
					',accuracy:', sameGroupBranch/counter



