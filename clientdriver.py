# File	: clientdriver.py
# Created by : Ade Surya R., Atika Firdaus, Sri Umay N. S.
# Description :
# clientdriver.py merupakan source code dari elemen yang berfungsi sebagai client. Client akan mengirim request
# kepada salah satu node berupa bilangan n dan akan menerima response berupa bilangan prima ke-n

# Import library
import sys,json
import http.client

# Prosedur yang menerima input berupa IP dan port dari node yang akan diberikan request, serta index sebagai n,
# yang akan mengembalikan bilangan prima ke-n
def proses(ip,port,index):
	# Membuat koneksi antara client dengan node yang diberi request
	connect = http.client.HTTPConnection(ip + ":" + str(port))
	datas = {
		"ip" : ip,
		"port" : port,
		"index" : index
	}
	data = json.dumps(datas)

	# Mengirim request kepada node dalam bentuk HTTP post
	connect.request("POST","/" + "requestprime",data)
	respon = connect.getresponse()
	response = respon.read().decode('utf-8')
	print(response)

# Menerima input dari user berupa IP dan port dari node yang dituju serta index n
if __name__ == "__main__":
	ip = sys.argv[1]
	port = int(sys.argv[2])
	index = int(sys.argv[3])
	print(ip,port,index)
	proses(ip,port,index)