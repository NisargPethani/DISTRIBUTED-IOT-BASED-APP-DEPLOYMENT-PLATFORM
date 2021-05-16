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

location = (float(sys.argv[2]), float(sys.argv[3]))  

def bigger(x,y):
    if(x>=y):
        decider = "x"
    else:
        decider = "y"
    return decider


def route(m,decider,loc):
    
    xs = []
    ys = []

    x,y = loc    
    
    xs.append(x)
    ys.append(y)

    while(x!=0 or y!=0):        
        if(decider=="y"):
            if(loc[1]<0):
                y=round(y+0.2,2)
            else:
                y=round(y-0.2,2)
            x = round(y/m,2) 
        else:
            if(loc[0]<0):
                x=round(x+0.2,2)
            else:
                x=round(x-0.2,2)
            y=round(m*x,2)
        

        xs.append(x)
        ys.append(y)

    return xs, ys
      

x,y = location

if(x==0):
    decider="y"
    x,y  = abs(x),abs(y)
else:
    m = y/x
    x,y  = abs(x),abs(y)
    decider = bigger(x,y)

xs, ys = route(m,decider,location)

lenth_of_route = len(xs)

xs[lenth_of_route-1] = 0
ys[lenth_of_route -1] = 0

print("Going into While True:")

counter = 6
start_index = 0

whileflag = True

while True:
    
    try:       
        
        # print(host, port)
        ClientMultiSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ClientMultiSocket.connect((host, port))
        
        res = ClientMultiSocket.recv(1024)
        while True:


            counter -= 1

            if counter == 0:
                counter = 6

                start_index += 1
                if start_index == lenth_of_route:
                    start_index = 0  

            time.sleep(1)
            whileflag = False

            try:        
      
                
                Input = 'Start'
                
                sensor_data = []

                sensor_data.append(xs[start_index])
                sensor_data.append(ys[start_index])
                                
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
