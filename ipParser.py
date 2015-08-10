from geoip import geolite2
from subprocess import call
import argparse
import os
temporaryFileName = 'temp.txt'

def parseGraph(classifyType ,fileName):
	result = {}
	readFile = open(fileName,'r')

	for line in readFile:

		splitter = line.split()
		match = geolite2.lookup(splitter[2])

		if classifyType == 'continent':
			value = match.continent
		elif classifyType == 'country':
			value = match.country
			
		if result.get(value) == None:
			result[value] = [splitter[1]]
		else:
			result[value].append(splitter[1])
	readFile.close()
	return result

def printGroup(result): 

	index = 1
	for value in result.keys():
		print value,result[value]
		writeFile = open('hight'+str(index)+'.txt','w')
		for data in result[value]:
			writeFile.write(data+'\n');
		index += 1
		writeFile.close();
	print "size: ",len(result)


def parseFile(fileName,time):
	
	readFile = open(fileName,'r')
	tempFile = open(temporaryFileName,'w')

	for line in readFile:
		split = line.split()	
		if int(split[0]) == time:
			tempFile.write(line)
		elif int(split[0]) > time:
			break;

	readFile.close()
	tempFile.close()

def getGraphFile():

	content = os.listdir('.')
	listSet = []
	for item in content:
		if item.startswith('hight'):
			listSet.append(item +' ')
	return ''.join(listSet)

def drawGraph(topoTime,hightLight,topoType):
	
	for index in range(0,4):
		os.system( './topo GROUP '+topoTime+'-topo'+str(index)+'.txt '+topoTime+'-'+topoType+str(index)+'.jpeg ' + hightLight)

def genTopologyFile(topoName,topoTime):
	os.system('python ParseTopoFile.py '+topoName+' '+topoTime+' 0-30')

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t',help='Input country or continent', type=str,choices=['country','continent'],required=True)
	parser.add_argument('-n',help='Input the client data file name(client_data_of_chn_1.txt)',type=str,required=True)
	parser.add_argument('-k',help='Input the topology file name(content_strategy1.txt)',type=str,required=True)
	parser.add_argument('-a',help='Input the topology file time(content_strategy1.txt)',type=str,required=True)
	args = parser.parse_args()

	if args.t:
		topoFileTime = args.a.split('-')
		clientFileTime = (int(topoFileTime[0]) * 60 + int(topoFileTime[1])) /3
		parseFile(args.n,clientFileTime)
		result = parseGraph(args.t, temporaryFileName)		
		printGroup(result)
		fileSet = getGraphFile()
		genTopologyFile(args.k, args.a)
		drawGraph(args.a,fileSet,args.t)
	else:
		print 'what the fuck,args.t: ',args.t,",args.n: ",args.n

