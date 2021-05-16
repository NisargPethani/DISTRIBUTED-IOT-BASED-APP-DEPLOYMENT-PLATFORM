from kafka import KafkaProducer
import socket
import os
from _thread import *
import random
import time
import mysql.connector
import sensor_instance_id
import threading
import json
import heart_beat_client
from requests import get
import kafka_topic

print()
print()
print()
print()
print("*******************************************************************")
print(get('https://api.ipify.org').text)
print("*******************************************************************")
print()
print()
print()
print()
print()

heart_beat_client.start_heart_beat()

def read_json_kafka(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    ip = data["ip"]
    port = data["port"]

    return ip, port

    # filepath = "configuration/kafka_config.json"
    # kafka_ip, kafka_port = read_json_kafka(filepath)

ServerSideSocket = socket.socket()

def get_host_ip_port(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())['sensor_server']

    ip = data["ip"]
    port = 50000

    return ip, port

filepathhost = "configuration/services_config.json"
host, port = get_host_ip_port(filepathhost)
host = "0.0.0.0"

ThreadCount = 0
try:
    ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("*******************************************************")
    print("Server:", host, port)
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(25)

def read_json_db(filepath):
    f = open (filepath, "r")
    data = json.loads(f.read())

    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]
    return host_name, user_name, password, database_name


def list_serializer(data):
    return str(data).encode("utf-8")


def fun(ip, port):
    # sensorinstanceipport
    # def db_connection(filepath):
    filepath = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    sql = "SELECT id FROM sensorinstanceipport where ip='"+ip+"' and port="+str(port)+""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    try:
        id = myresult[0][0]
        return [True, id]
    except Exception:
        id = -1
        return [False, id]

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        #data = 'Asdfg'
        #response = 'Server message: ' + data.decode('utf-8')
        response = str(data.decode('utf-8'))
        response = response.split(':::')
        sensor_ip = response[0]
        sensor_port = response[1]
        sensor_data = response[2]
        # sensor_data = []
        # data1 = int(response[2])
        # sensor_data.append(data1)
        # data1 = response[3]
        # sensor_data.append(data1)
        
        # print(sensor_ip)
        # print(sensor_port)
        # print(sensor_data)

        ######## logic to get uuid from ip and port and thus uuid will specify the topic of kafka


        filepathkafka = "configuration/kafka_config.json"
        kafka_ip, kafka_port = read_json_kafka(filepathkafka)

        producer = KafkaProducer(bootstrap_servers=['{}:{}'.format(kafka_ip,kafka_port)],
                                 value_serializer=list_serializer
                                )
        
        return_flag, id = fun(sensor_ip, sensor_port)
        if return_flag ==False:
            connection.close()
            return

        print("Inserting to Kafka: ", id, sensor_data)
        producer.send(id, sensor_data)
        # if sensor_port == '2020':
        #     producer.send("example_topic",sensor_data)
        # if sensor_port == '2030':
        #     producer.send("example_topic2",sensor_data)
        n = str(random.randint(1,50))
        connection.sendall(str.encode(n))
        #connection.sendall(str.encode(response))
    connection.close()

def topic_creator():
    while True:
        s_id = sensor_instance_id.get_id()
        kafka_topic.create_topic(s_id)

def sensor_binder():
    while True:

        # print("Sensor Binder Waiting State")
    
        Client, address = ServerSideSocket.accept()
        # print('*****************************Connected to: ' + address[0] + ':' + str(address[1]))
        threading.Thread(target=multi_threaded_client, args=(Client,)).start()

# threading.Thread(target=topic_creator).start()
threading.Thread(target=sensor_binder).start()
