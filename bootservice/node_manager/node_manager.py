## Node manager 
# from kafka import KafkaProducer, KafkaConsumer 
from datetime import datetime
from time import sleep
from json import loads 
import json
import sys
import socket
import threading
import os
import heart_beat_client
import mysql.connector
import json
from  node_db_queries import *
from requests import get
from kafka import KafkaConsumer, KafkaProducer

print()
print()
print()
print()
print("*******************************************************************")
print("Node Manager:", get('https://api.ipify.org').text)
print("*******************************************************************")
print()
print()
print()
print()
print()



def get_kafka_service_details(kafka_file_path):
	f = open (kafka_file_path, "r")
	data = json.loads(f.read())
	# kafka_ip = ""
	# kafka_port = "9092"

	kafka_ip = data['ip']
	kafka_port = data['port']
	return kafka_ip, kafka_port

def deregister_to_heart_beat_manager(ip, port, kafka_file_path): ## deregister
	request_type = 'deregister'
	print("\n----------------De-registration with Heart Beat Manager---------------------\n")
	kafka_ip, kafka_port = get_kafka_service_details(kafka_file_path)
	topic_name = "register_deregister"

	message = "{} {}-{}_{}".format(request_type, "node", ip, port)
	print("Application {} message : {}\n".format(request_type,message))

	producer = KafkaProducer(bootstrap_servers = ['{}:{}'.format(kafka_ip, str(kafka_port))], 
	api_version = (0,10,1))
	print("Topic name :",topic_name)
	producer.send(topic_name, json.dumps(message).encode('utf-8'))


#create and send the new node. <ip and port>
def create_new_node():
    if (len(fetch_free_node()) >0):    
        new_node = (fetch_free_node())[0]
        return new_node
    return ""


def form_string(ip_port_list):
    print("IP port list :", ip_port_list)
    string = ""
    for i in range(len(ip_port_list) -1):
        ip = ip_port_list[i][0]
        port = str(ip_port_list[i][1])
        user = ip_port_list[i][2]
        string = string + "{} {} {}:".format(ip,port, user)
    # handle last ip_port.
    length = len(ip_port_list)
    ip = ip_port_list[length -1][0]
    port = str(ip_port_list[length -1][1])
    user = ip_port_list[length -1][2]
    string = string + "{} {} {}".format(ip,port,user)
    return string



# return active node. <ip and port>
def get_active_node_list(message_content):
        print("Message_content :",message_content)

        send_message = ""

        if message_content == "node_list":
            ## form the string
            print("Hello inside nodelist")
            active_node_list = fetch_active_nodes()
            send_message = "{};{}".format('multiple', form_string(active_node_list))
            print("Message to send :", form_string(active_node_list))
        elif message_content == "new_node":
            ## get a new node and 
            new_node = create_new_node()
            if new_node != "":
                # active_node_list.append(new_node)
                ip = new_node[0]
                port = new_node[1]
                user = new_node[2]
                set_active(ip, port,user)
                temp_list = [new_node]
                send_message = "{};{}".format('single', form_string(temp_list))
            else:
                active_node_list = fetch_active_nodes()
                send_message = "{};{}".format('multiple', form_string(active_node_list))
        else:
            print("Hello no if else")
        
        send_message.rstrip()

        if send_message == "":
            print("send_mesaage is empty")
        print("Message send is :",send_message)
        return send_message

def add_new_node(ip,port, user):
    # ip_port_tuple = (ip, port)
    active_node_list = fetch_active_nodes()
    print("Active node list :", active_node_list)
    if (len(active_node_list)<2):
        # active_node_list.append(ip_port_tuple)
        insert_active_node(ip, port, user)
        print("inside new tuple active")
    else:
        # free_node_list.append(ip_port_tuple)
        insert_free_node(ip, port,user)
        print("inside new tuple free")

    # print(active_node_list)
    # print(free_node_list)

def handle_request(connection, client_address):
    request = connection.recv(1024).decode()
    request_array = request.split()
    request_from = request_array[0]
    err_message = "ERROR"
    # identify the request ie from the client or the sensor_server
    try:
        if request_from == 'deployer':
            print("Request For : ", request_from)

            if len(request_array) !=2:
                err_message = err_message +" "+ "Invalid number of arguments provided, two expected."
                connection.sendall(err_message.encode())
            message_content = request_array[1] # node_list or new_node
            response = get_active_node_list(message_content)
            
            connection.sendall(response.encode())
        elif (request_from == 'node'):
            print("request_array :", request_array)
            ip = request_array[1]
            port = int(request_array[2])
            user = request_array[3]
            print("Till here  -------------------------------------------")
            add_new_node(ip,port, user)
        elif (request_from == 'fault_tolerance'):
            print("------------ Delete Node Request From Fault Tolerence ------------------")
            # delete the node from the database.
            delete_node_ip = request_array[1]
            delete_node_port = int(request_array[2])
            set_deleted(delete_node_ip, delete_node_port)
            kafka_file_path = "./configuration/kafka_config.json"
            deregister_to_heart_beat_manager(delete_node_ip, delete_node_port, kafka_file_path)

            
        else :
            #connection.close()
            err_message = err_message +" "+ "Invalid request type."
            connection.sendall(err_message.encode())



    except AttributeError as error:
        print(error)
        connection.sendall(('ERROR :' + str(error)).encode())
    except TypeError as error:
        print(error)
        connection.sendall(('ERROR :' + str(error)).encode())


def server(server_ip, server_port):
    try:
        sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as error:
        print(error)
        exit(0)
    sockt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sockt.bind((server_ip, server_port))
        print('Socket is listening at ip : {}, port : {}'.format(server_ip, server_port))
        sockt.listen(10)

        while True:
            connection, client_address = sockt.accept()
            print("Got connection request from :{}".format(client_address))
            thread = threading.Thread(target=handle_request, args=(connection, client_address))
            thread.start()

    except socket.error as error:
        print(error)
    finally:
        sockt.close()

if __name__ == "__main__":
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    # thread = threading.Thread(target=heart_beat_client.heart_beat)
    # thread.start()
    heart_beat_client.start_heart_beat()
    server(server_ip, server_port)
    