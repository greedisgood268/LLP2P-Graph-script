from geoip import geolite2

readFile = open('temp.txt','r')
result = {}

for line in readFile:
	splitter = line.split()
	match = geolite2.lookup(splitter[2])
	value = result.get(match.continent)
	if value == None:
		value = [splitter[1]]
		result[match.continent] = value
	else:
		value.append(splitter[1])

index = 1
for value in result.keys():
	writeFile = open('hight'+str(index)+'.txt','w')
	for data in result[value]:
		writeFile.write(data+'\n');
	index += 1
	writeFile.close();
print "size: ",len(result)
readFile.close()

