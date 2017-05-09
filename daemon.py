#!/usr/bin/env python
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

PORT = 13336

listPort = [13338,13339,13340]
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

@threaded
def monitor():
	threading.Timer(5,monitor).start()
	st = str(psutil.virtual_memory())
	# print(psutil.virtual_memory())
	idx = st.find("percent=");
	idx1 = st.find("=",idx);
	idx2 = st.find(",",idx);
	st = st[idx1+1:idx2]
	print('data sending.......')
	for objport in listPort:
		# url = 'http://localhost:' + str(objport) + '/api'
		connect = http.client.HTTPConnection("127.0.0.1:" + str(objport))
		datas = {
			'data' : st,
			'sender_ip' : '127.0.0.1',
			'sender_port' : PORT
		}
		# print(data)
		# response = requests.post(url,json=data)
		try:
			data = json.dumps(datas)
			connect.request("POST","/" + "api",data)
			respon2 = connect.getresponse()
			data2 = respon2.read()
			print('response : ' + data2.decode("utf-8"))
		except:
			print('cannot send to node')
			pass
		# print(respon1.status,respon1.reason,respon1.getheaders())
		
	# response gak ada gimana ?

class DaemonHandler(BaseHTTPRequestHandler):
	# def getworker(self):
	# 	# connect = http.client.HTTPConnection("127.0.0.1:13337")
	# 	# connect.request("GET","/1")
	# 	# respon1 = connect.getresponse()
	# 	return "test2"
	def getCPULoad(self):
		st = str(psutil.virtual_memory())
		# print(psutil.virtual_memory())
		idx = st.find("percent=");
		idx1 = st.find("=",idx);
		idx2 = st.find(",",idx);
		st = st[idx1+1:idx2]
		return st
	def getIP(self):
		f = urllib.request.urlopen("http://ipecho.net/plain")
		ip = str(f.read())
		ipadr = ip[2:len(ip)-1]
		return ipadr+"\n"
	def getPort(self):
		return PORT
	def getworker(self,n):
		connect = http.client.HTTPConnection("127.0.0.1:13337")
		connect.request("GET","/" + str(n))
		respon1 = connect.getresponse()
		data1 = respon1.read().decode('utf-8')
		# print(primaread)
		# print(data1)
		return data1
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