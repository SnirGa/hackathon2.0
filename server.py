import socket
import threading
import struct
import time
class server:
    def __init__(self):
        self.port=2031
        self.IP=socket.gethostbyname(socket.gethostname())
        self.format='utf-8'
        self.tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.udp_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.udp_socket.bind('localhost',13117) #check!!!
        self.teams=[]
        self.udp_port=13117
        self.buffer=1024
        self.develop_net ="172.1.255.255" #socket.gethostbyname(socket.gethostname())

    
    def start_broadcast(self):
        print(f"server: start_broadcast method, IP {self.IP}")

        threading.Timer(1.0,self.start_broadcast).start()
        msg = struct.pack("Ibh",0xabcddcba,0x2,self.port)
        self.udp_socket.sendto(msg,(self.develop_net,self.udp_port)) #send port to connnect to TCP
        #msg="hello world".encode()
        #addr=(self.develop_net,self.udp_port)
        #self.udp_socket.sendto(msg,addr)

    def wait_for_clients(self):
        print("server: wait_for_clients method")

        thread=threading.Thread(target=self.start_broadcast)
        thread.start()
        while len(self.teams)<2:
            if len(self.teams)==1:
                print(f"{self.teams[0][2]} entered")
            self.tcp_socket.settimeout(0.1)
            try:
                client,address=self.tcp_socket.accept()
                group_name=client.recv(self.buffersize).decode("utf-8")
                tup=(client,address,group_name)
                self.teams.append(tup)
                print(f'{group_name} entered the game!')
            except:
                continue
        start_game()
    
    def game(self,client):
        print("server: game method")
        time.sleep(10)
        self.tcp_socket.listen()




        


    def start(self):
        print(f"Server started, listening on IP address {self.IP}")
        self.wait_for_clients()

def math_questions_dict():
    QA={}
    for i in range(10):
        for j in range(10):
            if i+j<10:
                QA[f'{str(i)}+{str(j)}']=i+j
            if i*j<10:
                QA[f'{str(i)}*{str(j)}']=i*j
            if i-j<10 and i>j:
                QA[f'{str(i)}-{str(j)}']=i-j
            if j!=0 and i%j==0 and i/j<10:
                QA[f'{str(i)}*{str(j)}']=i*j
    return QA




if __name__=='__main__':
    QA=math_questions_dict()
    s=server()
    s.start()
    connection=False
    while connection!=True:
        try:
            s.tcp_socket.bind("",s.port)
            connection=True
        except:
            pass
    s.tcp_socket.listen()
    while True:
        s.teams = [] #empty team
        print(f"Server started,listening on IP address {s.IP}") #start server
        s.wait_for_clients() #start sending UDP offers until 2 clients connected
        if len(s.teams)==2:
            dict_len=len(QA)
            rand_num=random.random(0,dict_len)
            question=list(QA.keys())[rand_num]
            answer=rand_num[question]

            first_group=s.teams[0][2]
            second_group=s.teams[1][2]
            welcome=f"Welcome to Quick Maths.\nPlayer 1: {first_group}\nPlayer 2:{second_group}\n==\n" \
                f"Please answer the following question as fast as you can:\nHow much is {question}?"
            
            for player in s.teams:
                player[0].send(bytes(welcome,'utf-8'))
                
            print(welcome)


            
            

        





