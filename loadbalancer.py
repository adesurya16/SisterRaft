# File  : loadbalancer.py
# Created by : Ade Surya R., Atika Firdaus, Sri Umay N. S.
# Description :
# loadbalancer.py merupakan source code dari load balancer yang berfungsi untuk mengatur segala aktivitas
# dari node, yaitu mengimplementasikan algoritma konsensus raft untuk menjadikan log seluruh node konsisten

# Import library
import urllib,sys
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import http.client
import json
import sys
import threading
import time

PORT = 0
TIMEOUT = 0

# List dari seluruh port node
listPort = [13338,13339,13340]

beginTime = time.time()

# Boolean follower, candidate, dan leader untuk menyimpan status dari node
isFollower = True
isCandidate = False
isLeader = False

# Term awal dari node
term = 0

# Variabel untuk menyimpan jumlah vote yang diterima
vote = 0

# isVote untuk menyimpan informasi apakah node telah memberikan vote dalam suatu leader election
isVote = False

# Variabel untuk menyimpan sementara log temporary dari follower sebelum dicommit
tmp_list = []

# Untuk melakukan threading
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

# Kelas get post handler untuk mengatur aktivitas node
class GetPostHandler(BaseHTTPRequestHandler):
    # Mengirim heartbeat pada seluruh node followers
    @threaded
    def appendEntries(self):
        global listPort,PORT,term
        while True:
            # Append entries menandakan leader masih aktif
            for objport in listPort:
                if not objport==PORT:
                    try:
                        connect = http.client.HTTPConnection("127.0.0.1:" + str(objport))
                        connect.request("GET","/" + str(term))
                        respon = connect.getresponse() # Heartbeat time
                    except:
                        pass
    
    # Merespon kepada vote yang diminta
    def responseVote(self,senderterm):
        # Reset begin time
        global term,isVote,beginTime
        print("term : " + str(term))
        beginTime = time.time()
        if senderterm > term and not isVote:
            # term = term + 1
            print('vote')
            isVote = True
            return '+'
        else:
            return '-'

    # Mengirim request vote pada setiap node yang ada
    def requestVote(self):
        global listPort,PORT,term,vote,isVote,isFollower,isLeader,isCandidate

        # Term dari node candidate yang melakukan request vote bertambah 1
        term = term + 1

        # Jumlah vote di awal adalah satu dari dirinya sendiri
        vote = 1

        # Mengirim pesan request vote ke seluruh node yang ada
        for objport in listPort:
            if not objport==PORT:
                print('request vote')
                connect = http.client.HTTPConnection("127.0.0.1:" + str(objport))
                datas = {
                    "ip" : "localhost",
                    "port" : PORT,
                    "term" : term
                }
                data = json.dumps(datas)
                try:
                    connect.request("POST","/" + "requestvote",data)
                    respon = connect.getresponse()
                    response = respon.read().decode('utf-8')

                    # Nilai vote bertambah satu ketika node memberi respon berupa "+"
                    if response == "+":
                        vote +=1
                except:
                    print("failed connecting")
                    pass
        print("term : " + str(term))
        print('vote : ' + str(vote))

        # Jika total vote yang diterima lebih dari sama dengan jumlah majority dari seluruh node, maka node menjadi leader
        if vote > (len(listPort) - 1) / 2:
            print('I`m a Leader now')
            isVote = False
            isFollower = False
            isCandidate = False
            isLeader = True
            self.appendEntries()
        else:
            isVote = False
            isFollower = True
            isCandidate = False
            isLeader = False

    # Merespon pada heartbeat yang diterima dari leader
    def responseAppendEntries(self):
        global beginTime,isVote
        isVote = False
        beginTime = time.time() # Reset waktu time election

    # Memberi respon kepada leader untuk menandakan node telah mengupdate lognya secara temporer sesuai update dari leader
    def responseCommit(self,datas):
        global tmp_list
        data = json.dumps(datas)
        tmp_list.append(data)
        return "+"

    # Fungsi untuk menyimpan log ke file eksternal
    def savefile(self,data):
        global PORT
        file = open('save_' + str(PORT),'r')
        vector = json.load(file) # Bentuk list atau dict
        file.close()
        file = open('save_' + str(PORT),'w')
        vector.extend(data)
        json.dump(vector,file)
        file.close()

    # Fungsi untuk menyimpan log ke file eksternal
    def replaceFile(self,data):
        global PORT
        file = open('save_' + str(PORT),'w')
        # vector.extend(data)
        json.dump(data,file)
        file.close()
    
    # Memberi kabar pada follower bahwa akan ada perubahan data
    def sendCommit(self,data):
        global listPort,PORT,term,vote,isVote,isFollower,isLeader,isCandidate,tmp_list
        # data = json.loads(data)
        # print(data['data'])
        # print('my tmp_list now :' + str(tmp_list))
        commit = 1
        datas = {
            "ip" : data['sender_ip'],
            "port" : data['sender_port'],
            "data" : data['data'],
            "term" : term
        }
        data = json.dumps(datas)
        tmp_list.append(data)
        for objport in listPort:
            if not objport==PORT:
                print('request commit')
                connect = http.client.HTTPConnection("127.0.0.1:" + str(objport))        
                # print(data)
                try:
                    connect.request("POST","/" + "requestcommit",data)
                    respon = connect.getresponse()
                    response = respon.read().decode('utf-8')
                    # response = request.post(url,json=data).decode('utf-8')
                    if response == "+":
                        commit +=1
                except:
                    pass
        print('commit : ' + str(commit))

        # Jika total commit yang diterima lebih dari sama dengan jumlah majority dari seluruh node, maka leader menyimpan
        # perubahan secara permanen dan memerintah follower untuk melakukan hal yang sama
        if vote > (len(listPort) - 1) / 2:
            # Send change
            print('I can send my changes')
            self.sendChange()
    
    # Mengambil data dari log
    def getdatasfromlog(self):
        global PORT
        # global TIMEOUT
        file = open('save_' + str(PORT),'r+')
        vector = json.load(file) #bentuk list atau dict
        file.close()
        return vector

    # Memberi kabar pada follower untuk menyimpan perubahan secara permanen
    def sendChange(self):
        global PORT,listPort,tmp_list
        datas = self.getdatasfromlog()
        # print(datas)
        self.savefile(tmp_list)
        print('logs added successfully')
        # print(self.getdatasfromlog())
        tmp_list = []
        for objport in listPort:
            if not objport==PORT:
                print('request change')
                try:
                    connect = http.client.HTTPConnection("127.0.0.1:" + str(objport))
                    data = json.dumps(datas)
                    connect.request("POST","/" + "responsechange",data)
                    response = connect.getresponse()
                    response = respon.read().decode('utf-8')
                except:
                    pass
        # datas.append(data)

    # Memberi respon kepada leader untuk menandakan data yang dimaksud telah dimasukkan ke dalam log node secara permanen
    def responseChange(self,datas):
        global tmp_list
        datas.extend(tmp_list)
        tmp_list = []
        self.replaceFile(datas)
        print('logs added successfully')
        return "+"

    # Mengurutkan log secara descending berdasarkan term
    def log_sort(self, seq):
        # bubble sort
        changed = True
        while changed:
            changed = False
            for i in range(0,len(seq)-2):
                # print('iterasi ke - ' + str(i))
                # print(seq[i]['term'])
                # print(seq[i+1]['term'])
                if seq[i]['term'] < seq[i+1]['term']:
                    seq[i], seq[i+1] = seq[i+1], seq[i]
                    changed = True
        return seq


    # Mengurutkan log secara ascending berdasarkan CPU load
    def cpu_load_sort(self, seq):
        # buble sort
        changed = True
        while changed:
            changed = False
            for i in range(len(seq) - 2):
                if seq[i]['data'] > seq[i+1]['data']:
                    seq[i], seq[i+1] = seq[i+1], seq[i]
                    changed = True
        return seq

    # Fungsi untuk mengembalikan list berupa log terakhir dari setiap server yang ada
    def getSmallestLoad(self):
        file = open('save_' + str(PORT), 'r+')
        vector = json.load(file)
        file.close()

        for i in range(len(vector)):
            vector[i] = json.loads(vector[i])
        sorted_vector = self.log_sort(vector)
        myList = []
        for obj in sorted_vector:
            if self.findInList(myList, obj['ip']) == False:
                myList.append(obj)
        min_cpu_load = self.cpu_load_sort(myList)
        return min_cpu_load

    def findInList(self, mylist, elmt):
        isInList = False
        if len(mylist) != 0:
            for obj in mylist:
                if obj['ip'] == elmt:
                    isInList = True
        return isInList

    def requestPrima(self,index):
        # dapatkan ip dan port yang terkecil cpu usagenya
        prima = 0
        datas = self.getSmallestLoad()
        print("datas : " + str(datas))
        isFound = True
        ip = ""
        port = 0
        for obj in datas:
            if prima == 0:
                ip = obj['ip']
                port = obj['port']
                try:
                    # print("ip : " + ip)
                    # print("port" + str(port))
                    connect = http.client.HTTPConnection(ip + ":"+ str(port))
                    connect.request("GET","/" + str(index))
                    # print('pass connect')
                    response = connect.getresponse().read()
                    # print('pass response')
                    print(response)
                    # respon1 = connect.getresponse()
                    # data1 = respon1.read().decode('utf-8')

                    # jsonparse = json.loads(response)
                    prima = int(response.decode('utf-8'))
                except:
                    print('exception request ke daemon/worker')
                    pass

        #request ke daemon (nanti daemon dapet prima dari worker)
        if isFound:
            data = {
                "prima" : prima,
                "port" : port,
                "ip" : ip
            }
            return str(data)
        else:
            return "0"

    # Mengambil hasil dari koneksi HTTP get yang dilakukan dengan node lain
    def do_GET(self):
        # global beginTime
        global term
        try:
            args = self.path.split('/')
            if args[1] == 'api':
                self.send_response(200)
                self.end_headers()
                self.wfile.write('wtf'.encode('utf-8'))
            elif args[1] == 'requestvote':
                self.send_response(200)
                self.end_headers()
                self.requestVote()
            elif args[1] == 'sendAppendEntries':
                self.send_response(200)
                self.end_headers()
                self.responseAppendEntries()
            else:
                if len(args) != 2:
                    raise Exception()
                n = int(args[1])
                term = n
                self.send_response(200)
                self.end_headers()
                self.responseAppendEntries()

        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

    # Mengambil hasil dari koneksi HTTP post yang dilakukan dengan node lain
    def do_POST(self):
        global isFollower,isCandidate,isLeader
        try:
            args = self.path.split('/')
            if args[1] == 'api': #menangani kiriman daemon
                length = int(self.headers['Content-Length'])
                # print("HEADERS: ", self.headers)
                # print (str(length))

                data = self.rfile.read(length).decode('utf-8')
                # print(data)
                if isLeader:
                    jsonparse = json.loads(data)
                    # print("get data from daemon (committed): " + str(jsonparse))
                    # print(jsonparse['data'])
                    self.sendCommit(jsonparse)
                    # self.savefile(data)
                # post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
                # print(post_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(('thanks daemon').encode('utf-8'))
            if args[1] == 'requestvote':
                length = int(self.headers['Content-Length'])
                # print("HEADERS: ", self.headers)
                # print (str(length))
                data = self.rfile.read(length).decode('utf-8')
                self.send_response(200)
                self.end_headers()
                # print(data)
                jsonparse = json.loads(data)
                self.wfile.write(self.responseVote(jsonparse['term']).encode('utf-8'))
            if args[1] == 'requestcommit':
                length = int(self.headers['Content-Length'])
                # print("HEADERS: ", self.headers)
                # print (str(length))
                data = self.rfile.read(length).decode('utf-8')
                self.send_response(200)
                self.end_headers()
                # print("request commit" + str(data))
                jsonparse = json.loads(data)
                self.wfile.write(self.responseCommit(jsonparse).encode('utf-8'))
            if args[1] == 'responsechange':
                length = int(self.headers['Content-Length'])
                # print("HEADERS: ", self.headers)
                # print (str(length))
                datas = self.rfile.read(length).decode('utf-8')
                self.send_response(200)
                self.end_headers()
                # print(datas)
                jsonparse = json.loads(datas)
                self.wfile.write(self.responseChange(jsonparse).encode('utf-8'))
            if args[1] == 'requestprime':
                length = int(self.headers['Content-Length'])
                # print("HEADERS: ", self.headers)
                # print (str(length))
                datas = self.rfile.read(length).decode('utf-8')
                self.send_response(200)
                self.end_headers()
                jsonparse = json.loads(datas)
                # panggil fungsi requestprima
                prima = jsonparse['index']
                print('prima : ' + str(prima)) 
                self.wfile.write(self.requestPrima(prima).encode('utf-8'))
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

class timeclass:
    # Mengubah status node menjadi candidate kemudian melakukan request vote
    @threaded
    def electionTimeOut(self):
        global TIMEOUT,isFollower,isCandidate,isLeader,beginTime,PORT,term,isVote
        while True: 
            if isFollower:
                currentTime = time.time()
                if currentTime - beginTime >= TIMEOUT:
                    beginTime = currentTime
                    print("timeout : " + str(TIMEOUT))
                    
                    # jadi candidate
                    isFollower = False
                    isCandidate = True
                    isVote = False
                    connect = http.client.HTTPConnection("127.0.0.1:" + str(PORT))
                    connect.request("GET","/" + "requestvote")
                    respon = connect.getresponse()

    
def main(port,timeout):
    global PORT
    global TIMEOUT
    PORT = port
    TIMEOUT = timeout
    print(PORT,TIMEOUT)
    
    # harus dicek kalo udah ada gak usah diinit
    file = open('save_' + str(PORT),'w')
    vector = []
    json.dump(vector,file)
    file.close()

    # classobj = GetPostHandler()
    # handle = classobj.electionTimeOut()
    objtime = timeclass()
    server = HTTPServer(("", PORT), GetPostHandler)
    objtime.electionTimeOut()
    server.serve_forever()
    handle.join()
    # handle = server.electionTimeOut()
    
if __name__ == '__main__':
    port = int(sys.argv[1])
    timeout = int(sys.argv[2])
    main(port,timeout)