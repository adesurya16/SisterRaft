import http.client
import json
connect = http.client.HTTPConnection("127.0.0.1:13335")
connect.request("GET","/" + "api")
respon1 = connect.getresponse()
data1 = respon1.read()
print(respon1.status,respon1.reason,respon1.getheaders())
print(data1.decode("utf-8"))
datas = {"eventType": "AAS_PORTAL_START", "data": "wtf"}
data = json.dumps(datas)
connect.request("POST","/" + "api",data)
respon2 = connect.getresponse()
data2 = respon2.read()
print(respon1.status,respon1.reason,respon1.getheaders())
print(data2.decode("utf-8"))