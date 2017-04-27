#!/usr/bin/env python
import psutil
import urllib.request
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import http.client
import socket

PORT = 13336
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
		return st+"\n"	
	def getIP(self):
		f = urllib.request.urlopen("http://ipecho.net/plain")
		ip = str(f.read())
		ipadr = ip[2:len(ip)-1]
		return ipadr+"\n"
	def getPort(self):
		return PORT
	def do_GET(self):
		try:
			args = self.path.split('/')
			# if len(args) != 2:
			# 	raise Exception()
			# n = int(args[1])
			self.send_response(200)
			self.end_headers()
			# self.wfile.write(str('worker : ' + self.getworker))
			self.wfile.write(self.getCPULoad().encode('utf-8'))
			self.wfile.write(self.getIP().encode('utf-8'))
			self.wfile.write(str(self.getPort()).encode('utf-8'))
		except Exception as ex:
			self.send_response(500)
			self.end_headers()
			print(ex)
server = HTTPServer(("", PORT), DaemonHandler)
server.serve_forever()