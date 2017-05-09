# File	: loadbalancer.py
# Created by : Ade Surya R., Atika Firdaus, Sri Umay N. S.
# Description :
# loadbalancer.py merupakan source code dari load balancer yang berfungsi untuk mengatur segala aktivitas
# dari node, yaitu mengimplementasikan algoritma konsensus raft untuk menjadikan log seluruh node konsisten

# Import library
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

# List dari seluruh port node
listPort = [13338,13339,13340]

# Untuk melakukan threading
# Data yang didapat berbentuk list of object karena server bisa lebih dari satu
def threaded(fn):
	def wrapper(*args, **kwargs):
		thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
		thread.start()
		return thread
	return wrapper

# Kelas node handler untuk mengatur aktivitas node
class NodeHandler(BaseHTTPRequestHandler):
	# Boolean follower, candidate, dan leader untuk menyimpan status dari node
	follower = True
	candidate = False
	leader = False

	beginTime = 0
	
	# isVote untuk menyimpan informasi apakah node telah memberikan vote dalam suatu leader election
	isVote = False

	# Term awal dari node
	term = 1
	
	# Variabel untuk menyimpan sementara log temporary dari follower sebelum dicommit
	tempSave = []

	# Fungsi untuk menyimpan log ke file eksternal
	def saveFile(self,data):
		file = open('save_' + str(PORT),'r+')
		vector = json.load(file) #bentuk list atau dict
		# vector.append(data)
		vector.append(data)
		json.dump(vector,file)
		file.close()

	# Saat menjadi follower

	# Mengubah status node menjadi candidate kemudian melakukan request vote
	@threaded
	def electionTimeOut(self):
		currentTime = time.time()
		if follower and currentTime-beginTime > timeOut:
			follower = False
			candidate = True
			leader = False
			requestvote()
			beginTime = currentTime

	# Merespon kepada vote yang diminta
	def responVote(self,otherterm):
		beginTime = time.time()
		if otherterm>term:
			return "voted" 
		else: 
			return "unvoted"

	# Memberi respon kepada leader untuk menandakan node telah mengupdate lognya sesuai update dari leader
	def responCommit(self,data):
		beginTime = time.time()
		# Menyimpan data log di temporary variable
		tempSave.append(data)
		return "commited"

	# Memberi respon kepada leader untuk menandakan data yang dimaksud telah dimasukkan ke dalam log node secara permanen
	def responChange(self,data):
		# Mencari data yang akan disimpan permanen pada temporary data
		for temp in tempSave:
			if temp == data
				saveFile(temp)
				tempSave.remove(temp)
		beginTime = time.time()
		return "changed"

	# Saat menjadi candidate

	# Mengirim request vote pada setiap node yang ada
	def requestVote(self):
		# Term dari node candidate yang melakukan request vote bertambah 1
		self.term += 1

		# Variabel untuk menyimpan jumlah vote yang diterima
		vote = 0

		# Mengirim pesan request vote ke seluruh node yang ada
		for objport in listPort:
			if not objport==PORT:
				url = 'http://localhost:' + objport + '/responvote'
				data = {
					"sender_ip" : "localhost",
					"sender_port" : PORT,
					"sender_term" : term
				}
				response = requests.post(url,json=data)

				# Nilai vote bertambah satu ketika node memberi respon berupa "voted"
				if response == "voted":
					vote +=1

		# Jika total vote yang diterima lebih dari sama dengan jumlah majority dari seluruh node, maka node menjadi leader
		if vote > len(listPort) - 1 / 2:
			follower = False
			candidate = False
			leader = True
	
	# Saat menjadi leader

	# Memberi kabar pada follower bahwa akan ada perubahan data
	def sendCommit(self,data):
		# Variabel untuk menyimpan jumlah commit yang diterima
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

		# Jika total commit yang diterima lebih dari sama dengan jumlah majority dari seluruh node, maka leader menyimpan
		# perubahan secara permanen dan memerintah follower untuk melakukan hal yang sama
		if commit > len(listPort) - 1 / 2:
			sendChange(data)

	# Memberi kabar pada follower untuk menyimpan perubahan secara permanen
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

	# Mengambil hasil dari koneksi HTTP post yang dilakukan dengan node lain
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
    		# Cari dari log waktu terbaru dan load cpu
    		self.send_response(200)
            self.end_headers()
            self.wfile.write()

input(timeOut,PORT)
server = HTTPServer(("", PORT), NodeHandler)
handle = server.electiontime()
server.serve_forever()