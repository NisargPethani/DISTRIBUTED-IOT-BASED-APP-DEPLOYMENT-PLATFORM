import socket
import time
import random
from requests import get
import json
import sys

def read_json_kafka(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    ip = data["ip"]
    port = data["port"]

    return ip, port

def get_host_ip_port(filepath):
    f = open (filepath, "r")
  
    # Reading from file
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


print("Going into While True:")

while True:
    try:
        # ClientMultiSocket.bind(('127.0.0.1', 5500))
        print('0.0')
        print(host, port)
        ClientMultiSocket.connect((host, port))
        print('1')
        res = ClientMultiSocket.recv(1024)
        while True:
            try:

                print('2')
                #Input = input('Hey there: ')
                Input = 'Start'
                #Input = 'Sensor1:'+str(random.randint(1, 50))
                sensor_data = []
                sensor_data.append(random.randint(1,100))
                sensor_data.append('ABCD')
                Input = sensor_ip_database + ':::' + str(sensor_port) + ':::' + str(sensor_data)
                #Input = sensor_ip+':::'+str(sensor_port)+':::'+str(random.randint(1,100))+':::'+'ABCD'
                print(str(sensor_data))
                ClientMultiSocket.send(str.encode(Input))
                res = ClientMultiSocket.recv(1024)
                #print(res.decode('utf-8'))
                time.sleep(4)
            except:
                flag_x = True
                print('3')
                # time.sleep(4)
                break

    except socket.error as e:
        print('0.1')
        if flag_x:
            ClientMultiSocket.close()
            ClientMultiSocket = socket.socket()
            ClientMultiSocket.bind((sensor_ip, sensor_port))
            print('5')
            flag_x = False
        print('4')
        # time.sleep(4)
        pass
        #print(str(e))


ClientMultiSocket.close()
