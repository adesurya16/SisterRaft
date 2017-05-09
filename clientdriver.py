import sys,json
import http.client
def proses(ip,port,index):
	connect = http.client.HTTPConnection(ip + ":" + str(port))
	datas = {
		"ip" : ip,
		"port" : port,
		"index" : index
	}
	data = json.dumps(datas)
	connect.request("POST","/" + "requestprime",data)
	respon = connect.getresponse()
	response = respon.read().decode('utf-8')
	print(response)

if __name__ == "__main__":
	ip = sys.argv[1]
	port = int(sys.argv[2])
	index = int(sys.argv[3])
	print(ip,port,index)
	proses(ip,port,index)