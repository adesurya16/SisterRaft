# File	: daemon.py
# Created by : Ade Surya R., Atika Firdaus, Sri Umay N. S.
# Description :
# daemon.py merupakan source code dari daemon yang berfungsi untuk mengumpulkan workload dari server
# untuk kemudian diberikan kepada node

# Import library
import psutil
import urllib.request
import requests	
import threading
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import http.client
import socket
import json
import time
from time import sleep

# Port dari daemon
PORT = 13336

# List dari seluruh port node
listPort = [13338,13339,13340]

# Fungsi yang mengembalikan IP dari daemon
def getIP():
		# f = urllib.request.urlopen("http://ipecho.net/plain")
		# ip = str(f.read())
		# ipadr = ip[2:len(ip)-1]
		hostname = socket.gethostname()
		IP = socket.gethostbyname(hostname)
		return IP

# Untuk melakukan threading
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

# Menghubungkan daemon dengan seluruh node yang berada di dalam listPort
@threaded
def monitor():
	threading.Timer(5,monitor).start()

	# Mengambil workload dari server berupa 
	st = str(psutil.virtual_memory())
	idx = st.find("percent=")
	idx1 = st.find("=",idx)
	idx2 = st.find(",",idx)
	st = st[idx1+1:idx2]
	print('data sending.......')
	
	# Menghubungkan daemon ke seluruh node yang ada di dalam listPort
	for objport in listPort:
		# url = 'http://localhost:' + str(objport) + '/api'

		# URL untuk melakukan HTTP Connection
		connect = http.client.HTTPConnection("127.0.0.1:" + str(objport))

		# Data menyimpan workload dari daemon, sender IP merupakan IP dari daemon, dan sender_port adalah port dari daemon
		datas = {
			'data' : float(st),
			'sender_ip' : '192.168.43.207',
			'sender_port' : PORT
		}
		# response = requests.post(url,json=data)

		# Menghubungkan daemon dengan node melalui HTTP post
		try:
			data = json.dumps(datas)
			connect.request("POST","/" + "api", data)
			respon2 = connect.getresponse()
			data2 = respon2.read()
			print('response : ' + data2.decode("utf-8"))
		except:
			print('cannot send to node')
			pass

		# print(respon1.status,respon1.reason,respon1.getheaders())
		
	# response gak ada gimana ?

# Kelas daemon handler untuk mengatur aktivitas daemon
class DaemonHandler(BaseHTTPRequestHandler):
	# def getworker(self):
	# 	# connect = http.client.HTTPConnection("127.0.0.1:13337")
	# 	# connect.request("GET","/1")
	# 	# respon1 = connect.getresponse()
	# 	return "test2"

	# Fungsi untuk mengambil workload dari CPU daemon
	def getCPULoad(self):
		st = str(psutil.virtual_memory())
		# print(psutil.virtual_memory())
		idx = st.find("percent=");
		idx1 = st.find("=",idx);
		idx2 = st.find(",",idx);
		st = st[idx1+1:idx2]
		return st

	# Getter untuk port daemon
	def getPort(self):
		return PORT

	# Fungsi untuk menghubungkan daemon kepada worker yang akan mengembalikan bilangan prima ke-n 
	def getworker(self,n):
		connect = http.client.HTTPConnection("127.0.0.1:13337")
		connect.request("GET","/" + str(n))
		respon1 = connect.getresponse()
		data1 = respon1.read().decode('utf-8')
		# print(primaread)
		# print(data1)
		return data1

	# Mengambil hasil dari koneksi HTTP get yang dilakukan dengan worker
	def do_GET(self):
		try:
			args = self.path.split('/')
			self.send_response(200)
			self.end_headers()
			# self.wfile.write(str('worker : ' + self.getworker))
			if len(args) != 2:
				raise Exception()
			n = int(args[1])
			self.wfile.write(str(self.getworker(n)).encode('utf-8'))
		except Exception as ex:
			self.send_response(500)
			self.end_headers()
			print(ex)

monitor()
server = HTTPServer(("", PORT), DaemonHandler)
server.serve_forever()