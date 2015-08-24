readSign = ['None','globalLift','Move','Lift']
sign = readSign.index('None')

moveCounter = 0
liftCounter = 0
globalLiftCounter = 0

readFile = open('record_strategy1.txt','r')

for line in readFile:
	
	if sign == readSign.index('globalLift'):

		if 'requestPeerToMove for pid:'	in line:
			globalLiftCounter = globalLiftCounter + 1				
		elif 'globalLift end,' in line:
			sign = readSign.index('Move')	

	elif sign == readSign.index('Move'):

		if 'globalLift begin' in line:
			sign = readSign.index('globalLift')
		elif 'requestPeerToMove for pid:'	in line:
			moveCounter = moveCounter + 1				
		elif 'optimizedTopology Move end' in line:
			sign = readSign.index('None')	

	elif sign == readSign.index('Lift'):

		if 'requestPeerToMove for pid:'	in line:
			liftCounter = liftCounter + 1				
		elif 'optimizedTopology Lift end' in line:
			sign = readSign.index('None')	

	elif sign == readSign.index('None'):	

		if 'optimizedTopology Move begin' in line:
			sign = readSign.index('Move')
		elif 'optimizedTopologyLift begin' in line:
			sign = readSign.index('Lift')
		else:
			pass

readFile.close()

print 'Move number:',moveCounter,',Lift number:',liftCounter,',globalLift number:',globalLiftCounter,',totalNumber:',moveCounter+liftCounter+globalLiftCounter
