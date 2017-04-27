import http.client
connect = http.client.HTTPConnection("127.0.0.1:13337")
x = input("prima : ")
connect.request("GET","/" + x)
respon1 = connect.getresponse()
data1 = respon1.read()
print(respon1.status,respon1.reason,respon1.getheaders())
print(data1.decode("utf-8"))