import socket
import time
import random
from requests import get
import json
import sys

def get_host_ip_port(filepath):
    f = open (filepath, "r")
  
    
    data = json.loads(f.read())['sensor_server']

    ip = data["ip"]
    port = 50000

    return ip, port

filepathhost = "configuration/services_config.json"
host, port = get_host_ip_port(filepathhost)

ClientMultiSocket = socket.socket()

sensor_ip = "0.0.0.0"
sensor_port = int(sys.argv[1])


sensor_ip_database =  get('https://api.ipify.org').text

print('Waiting for connection response')
flag_x = False
try:
    ClientMultiSocket.bind((sensor_ip, sensor_port))
except:
    pass

x = 500
step_x = 50

print("Going into While True:")

whileflag = True

while True:

    try:
                
        # print(host, port)
        ClientMultiSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ClientMultiSocket.connect((host, port))
        
        res = ClientMultiSocket.recv(1024)
        while True:      

            
            x = x + step_x
            if x > 850 or x < 150:
                step_x = -step_x
            
            # print(x)    

            time.sleep(1)
            whileflag = False  
            try:
                
                Input = 'Start'                
                sensor_data = []
                sensor_data.append(x)

                Input = sensor_ip_database + ':::' + str(sensor_port) + ':::' + str(sensor_data)
                
                print(str(sensor_data))
                ClientMultiSocket.send(str.encode(Input))
                res = ClientMultiSocket.recv(1024)
                
            except:
                flag_x = True    
                break

    except socket.error as e:
        
        if flag_x:
            ClientMultiSocket.close()
            ClientMultiSocket = socket.socket()
            ClientMultiSocket.bind((sensor_ip, sensor_port))
            
            flag_x = False
        
        pass    
	
    if whileflag:
        time.sleep(1)
    whileflag = True    

ClientMultiSocket.close()
