#firstTime = raw_input('Input the first time to compare:\n')
#secondTime = raw_input('Input the second time to compare:\n')
#firstTime = 2
#secondTime = 4
import sys

def parseFile(command):

	fileName = 'client_data_of_chn_1.txt'
	readFile = open(fileName,'r')
	value = [0.00,0.00,0.00,0.00,0.00]
	time = 0
	currentCheck = -1
	accumulateDelay = [0.00,0.00,0.00,0.00,0.00]
	accumulateTime = 0

	for line in readFile:
		result = line.split()
		if currentCheck != int(result[0]):
			printValue = [0.00,0.00,0.00,0.00,0.00]
			for streamIndex in range(0,5):
				if currentCheck != -1:
					printValue[streamIndex] = value[streamIndex]/time	
					accumulateDelay[streamIndex] += printValue[streamIndex] 

				value[streamIndex] = (float)(result[ 4 + streamIndex])
			if currentCheck != -1:
				accumulateTime += 1
				if command != -1:
					print printValue[command]
			currentCheck = int(result[0])
			time = 1

		else:
			for streamIndex in range(0,5):
				value[streamIndex] += (float)(result[ 4 + streamIndex])
			time = time + 1 
	
	printValue = [0.00,0.00,0.00,0.00,0.00]
	for streamIndex in range(0,5):
		printValue[streamIndex] = value[streamIndex]/time	
		accumulateDelay[streamIndex] += printValue[streamIndex] 

	if currentCheck != -1:
		accumulateTime += 1
		if command != -1:
			print printValue[command]

	readFile.close()	

	for streamIndex in range(0,5):
		accumulateDelay[streamIndex] /= accumulateTime

	print "Total average delay: ",accumulateDelay

if __name__ =='__main__':

	if len(sys.argv) > 1:
		parseFile(int(sys.argv[1]))
	else:
		parseFile(-1)

