import socket
import time
import random
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


sensor_ip2 = "1.2.3.4"
print('Waiting for connection response')
try:
    ClientMultiSocket.bind((sensor_ip, sensor_port))
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)
while True:
    #Input = input('Hey there: ')
    Input = 'Start'
    #Input = 'Sensor1:'+str(random.randint(1, 50))
    sensor_data = []
    sensor_data.append(random.randint(1,100))
    sensor_data.append('ABCD')
    Input = sensor_ip2 + ':::' + str(sensor_port) + ':::' + str(sensor_data)
    #Input = sensor_ip+':::'+str(sensor_port)+':::'+str(random.randint(1,100))+':::'+'ABCD'
    ClientMultiSocket.send(str.encode(Input))
    res = ClientMultiSocket.recv(1024)
    #print(res.decode('utf-8'))
    time.sleep(4)

ClientMultiSocket.close()