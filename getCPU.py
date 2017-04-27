import psutil
import socket
import urllib.request
# import json
# external_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')
# import requests
f = urllib.request.urlopen("http://ipecho.net/plain")
# print(f.read())
# r = requests.get(r'http://jsonip.com')
# ip = r.json()['ip']
# print(external_ip)
# data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
# print(data["ip"])
ip = str(f.read())
ipadr = ip[2:len(ip)-1]
st = str(psutil.virtual_memory())
print(psutil.virtual_memory())
idx = st.find("percent=");
idx1 = st.find("=",idx);
idx2 = st.find(",",idx);
st = st[idx1+1:idx2]
print(st)
print(socket.gethostbyname(socket.gethostname()))
print(socket.gethostbyname(socket.getfqdn()))
# print(my_ip)