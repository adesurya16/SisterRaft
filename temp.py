	def date_sort(self, seq):
		changed = True
		while changed:
			changed = False
			for i in range(len(seq) - 1):
				prevtime = time.strptime(seq[i].time, "%d/%m/%Y %H:%M:%S")
				nexttime = time.strptime(seq[i+1].time, "%d/%m/%Y %H:%M:%S")
				if prevtime < nexttime:
					seq[i], seq[i+1] = seq[i+1], seq[i]
					changed = True
		return None

	def getSmallestLoad(self):
		file = open('save_' + str(PORT), 'r+')
		vector = json.load(file)
		date_sort(vector)
		myList = []
		for obj in vector:
			if findInList(myList, obj.port) == False:
				myList.insert(obj)
		min_cpu_load = myList[i]
		for obj in myList[1:]:
			if obj.cpu_load < min_cpu_load.cpu_load:
				min_cpu_load = obj
		return min_cpu_load

	def findInList(self, mylist, elmt):
		isInList = False
		for i in range(len(mylist)):
			if mylist[i] == elmt:
				isInList = True
		return isInList