fileCluster = ['record_channel.txt','content_strategy1.txt','record_strategy1.txt']

def pareseFile(fileType):
	




if __name__ == '__main__':		
	print "The files able to be parsed are showed below"
	for index in range(len(fileCluster)):
		print fileCluster[index],',Input: ',index
	fileType = raw_input('Input the file number your want to parse(The file should be placed in the current directory)\n')

	time = raw_input('Input the time you want to search x-y (which means the starting from x minutes and y minutes)')
	duration = raw_input('Input the time duration you want to search x-y (which means the starting from x minutes and y minutes)')
	targetString = raw_input('Input the targetString')
	parseFile( fileType, time, duration)
