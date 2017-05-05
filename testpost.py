# import requests,json

# url = 'http://167.0.0.1:13335/api'

# datas = {"eventType": "AAS_PORTAL_START", "data": "wtf"}
# data = json.dumps(datas)
# # params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}
# print('tes')
# headers = {'Content-Type': 'application/json'}
# req = requests.post(url,data=data,headers=headers)
# req2 = requests.get(url)
# print('tes')
# print(req)
# print(req2)
import http.client
import json
connect = http.client.HTTPConnection("127.0.0.1:13335")
# x = input("prima : ")
# connect.request("GET","/" + "api")
# respon1 = connect.getresponse()
# data1 = respon1.read()
# print(respon1.status,respon1.reason,respon1.getheaders())
# print(data1.decode("utf-8"))
datas = {"eventType": "AAS_PORTAL_START", "data": "wtf"}
data = json.dumps(datas)
connect.request("POST","/" + "api",data)
respon2 = connect.getresponse()
data2 = respon2.read()
print(respon2.status,respon2.reason,respon2.getheaders())
print(data2.decode("utf-8"))