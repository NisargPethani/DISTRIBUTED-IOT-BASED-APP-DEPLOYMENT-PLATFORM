import socket
import time
import random
from _thread import start_new_thread
from kafka import KafkaConsumer
import mysql.connector
from json import loads
import json
from kafka.structs import TopicPartition
import threading
import heart_beat_client

from requests import get

print()
print()
print()
print()
print("*******************************************************************")
print("Controller Server:", get('https://api.ipify.org').text)
print("*******************************************************************")
print()
print()
print()
print()
print()

heart_beat_client.start_heart_beat()
def read_json_db(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]
    return host_name, user_name, password, database_name
    


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
    data = json.loads(f.read())['controller_server']

    ip = data["ip"]
    port = 60000

    return ip, port

filepathkafka = "configuration/kafka_config.json"
kafka_ip, kafka_port = read_json_kafka(filepathkafka)

def ip_port(id):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)

    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    
    sql = "SELECT ip, port FROM controllerinstanceipport where id='"+id+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    try:
        ip, port = myresult[0][0], myresult[0][1]
        return [True, ip, port]
    except Exception:
        ip = -1
        port = -1
        return [False, ip, port]

def send_msg_to_controller(message, controller_ip, controller_port):

    controller_ip = ""

    try:
        sock = socket.socket()
        sock.connect((controller_ip, controller_port)) 

        received_data = message.value.decode()
        print("********",received_data)
   
        # connect to the server on local computer 
        # receive data from the server 
        print("Sending on socket..........")
        sock.sendall(received_data.encode())
        sock.close()

    except socket.error as e:

        sock.close()
        print("*****************Controller signal error.... ", e, message.value.decode())

def controller_instance(controller_id):

    print("*********************************", "Redy to get reqest for ", controller_id)

    flag, controller_ip, controller_port = ip_port(controller_id)
    if not flag:
        print("Controller {} not working", controller_id)   
        return

    print(controller_ip, controller_port)

    consumer = KafkaConsumer(controller_id, 
                            bootstrap_servers = ['{}:{}'.format(kafka_ip,kafka_port)], 
                            api_version = (0,10)
                            )
  
    
    for message in consumer:

        print("Got New message for...", controller_ip, controller_port)
        print("Message", message.value.decode())
        
        threading.Thread(target=send_msg_to_controller, args=(message, controller_ip, controller_port)).start()

consumer = KafkaConsumer("appmanager_controllerserver",bootstrap_servers=['{}:{}'.format(kafka_ip,kafka_port)],api_version=(0,10))
s = socket.socket()

for message in consumer:
    print("********************************New Message")
    controller_id = message.value.decode()
    print(controller_id)
    threading.Thread(target=controller_instance, args=(controller_id,)).start()