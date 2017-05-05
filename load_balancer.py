from time import sleep
import requests
import urllib.request
import request
from threading import Thread
import json
import time
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


# nanti semua node di localhost dan port yang berbeda
PORT = 0
timeOut = 0
listPort = [13338,13339,13340]
# port semua node

# data yang didapet dari sini bentuknya list of object karena server  bisa banyak
def threaded(fn):
	def wrapper(*args, **kwargs):
		thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
		thread.start()
		return thread
	return wrapper

class NodeHandler(BaseHTTPRequestHandler):
	follower = True
	candidate = False
	leader = False
	beginTime = 0
	isVote = False
	term = 1
	tempSave = []

	def saveFile(self,data):
		file = open('save_' + str(PORT),'r+')
		vector = json.load(file) #bentuk list atau dict
		# vector.append(data)
		vector.append(data)
		json.dump(vector,file)
		file.close()

	# saat menjadi follower	
	@threaded
	def electionTimeOut(self):
		currentTime = time.time()
		if follower and currentTime-beginTime > timeOut:
			follower = False
			candidate = True
			leader = False
			requestvote()
			beginTime = currentTime

	def responVote(self,otherterm):
		beginTime = time.time()
		if otherterm>term:
			return "voted" 
		else: 
			return "unvoted"

	def responCommit(self,data):
		beginTime = time.time()
		# simpan data di temporer file
		tempSave.append(data)
		return "commited"

	def responChange(self,data):
		#mencari di temporery data
		for temp in tempSave:
			if temp == data
				saveFile(temp)
				tempSave.remove(temp)
		beginTime = time.time()
		return "changed"
	#candidate
	def requestVote(self):
		self.term += 1
		vote = 0
		for objport in listPort:
			if not objport==PORT:
				url = 'http://localhost:' + objport + '/responvote'
				data = {
					"sender_ip" : "localhost",
					"sender_port" : PORT,
					"sender_term" : term
				}
				response = requests.post(url,json=data)
				if response == "voted":
					vote +=1
		if vote > len(listPort) - 1 / 2:
			follower = False
			candidate = False
			leader = True
	
	#leader
	def sendCommit(self,data):
		commit = 0
		for objport in listPort:
			if not objport==PORT:
				url = 'http://localhost:' + objport + '/responcommit'
				data = {
					"data" : data,
					"sender_ip" : "localhost",
					"sender_port" : PORT
				}
				response = requests.post(url,json=data)
				if response == "commited":
					commit+=1
		if commit > len(listPort) - 1 / 2:
			sendChange(data)
	def sendChange(self,data):
		for objport in listPort:
			if not objport==PORT:
				url = 'http://localhost:' + objport + '/responchange'
				data = {
					"data" : data,
					"sender_ip" : "localhost",
					"sender_port" : PORT
				}
				response = requests.post(url,json=data)
	def do_POST(self):
        try:
        	length = int(self.headers['Content-Length'])
        	post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
            args = self.path.split('/')
            if args[1] == 'responvote':
            	self.send_response(200)
            	self.end_headers()  
            	self.wfile.write() #responvote kasih
            else if args[1] == 'responcommit':
            	self.send_response(200)
            	self.end_headers()
            	self.wfile.write()
            else if args[1] == 'responchange':
            	self.send_response(200)
            	self.end_headers()
            	self.wfile.write()
            else if args[1] == 'sendcpu':
            	for key,value in post_data.items():
            		print(value[key])
            	if leader:
            		sendCommit(post_data['data'])
            	self.send_response(200)
            	self.end_headers()
            	self.wfile.write("success")
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

    def do_GET(self):
    	try:
    		args = self.path.split('/')
    		n =  int(args[1])
    		# cari dari log waktu terbaru dan load cpu
    		self.send_response(200)
            self.end_headers()
            self.wfile.write()
# saat menjadi candidate


input(timeOut,PORT)
#saat menjadi leader
server = HTTPServer(("", PORT), NodeHandler)
handle = server.electiontime()
server.serve_forever()
# electiontime()
# port = 0
# port = read()
# PORT = port