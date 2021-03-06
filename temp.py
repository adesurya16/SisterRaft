	def log_sort(self, seq):
		changed = True
		while changed:
			changed = False
			for i in range(len(seq) - 1):
				if seq[i].term < seq[i+1].term:
					seq[i], seq[i+1] = seq[i+1], seq[i]
					changed = True
		return seq

	def cpu_load_sort(self, seq):
		changed = True
		while changed:
			changed = False
			for i in range(len(seq) - 1):
				if seq[i].cpu_load > seq[i+1].cpu_load:
					seq[i], seq[i+1] = seq[i+1], seq[i]
					changed = True
		return seq

	def getSmallestLoad(self):
		file = open('save_' + str(PORT), 'r+')
		vector = json.load(file)
		sorted_vector = log_sort(vector)
		myList = []
		for obj in sorted_vector:
			if findInList(myList, obj.port) == False:
				myList.insert(obj)
		min_cpu_load = cpu_load_sort(myList)
		return min_cpu_load

	def findInList(self, mylist, elmt):
		isInList = False
		for i in range(len(mylist)):
			if mylist[i] == elmt:
				isInList = True
		return isInList