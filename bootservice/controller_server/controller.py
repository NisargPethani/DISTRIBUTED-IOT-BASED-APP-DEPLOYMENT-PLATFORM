import socket
import os
import threading
import sys
from requests import get

controller_ip = "0.0.0.0"
controller_port = int(sys.argv[1])

# print("Controller Info", get('https://api.ipify.org').text, controller_port)

# s = socket.socket()   
# print ("Socket successfully created")
# print("Bindnig on.... ",controller_ip, controller_port)

# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind((controller_ip, controller_port))     

# s.listen(20)     
# print ("socket is listening")            

def serv_req(sock, client_address):

    print("Signal for Controller {}: {}".format(sys.argv[2], sock.recv(1024).decode()))
    sock.close()

# while True: 

#     sock, addr = s.accept()     
#     threading.Thread(target=serv_req, args=(sock,)).start()

print("NEW CONTROLLER.......")

try:
    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as error:
    print(error)
    exit(0)

sockt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sockt.bind((controller_ip, controller_port))
    print('Socket is listening at ip : {}, port : {}'.format(get('https://api.ipify.org').text, controller_port))
    sockt.listen(10)
    
    while True:
        connection, client_address = sockt.accept()
        # print("Got connection request from :{}".format(client_address))
        
        thread = threading.Thread(target=serv_req, args=(connection, client_address))
        thread.start()

except socket.error as error:
    print("Error.....", error)
finally:
    sockt.close()