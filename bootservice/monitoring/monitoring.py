import sys
import threading
from kafka import KafkaConsumer, KafkaProducer
from time import sleep
import json
import time
from datetime import datetime
from requests import get
from requests.api import request
import mysql
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


import json



		
registration_dict = {}	

db_config_filepath = "./configuration/db_config.json"

def read_json(filepath):
    f = open (filepath, "r")
    # Reading from file
    data = json.loads(f.read())

    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]
    return host_name, user_name, password, database_name

def fetch_node_status(node_ip,node_port):
    host_name, user_name, password, database_name = read_json(db_config_filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    free_node = [] 
    mycursor.execute("select ip, port, user from nodes where status='deleted' and ip = '{}' and port = '{}' limit 1;".format(node_ip, node_port))
    myresult = mycursor.fetchall()
    
    free_node = []
    for node in myresult:
        free_node.append((node[0], int(node[1]), node[2]))
    return free_node


def register(request_msg):
	component_id_list = request_msg.split('-', 1)	# component_id_list = ['node', 'ip_9200']
	if component_id_list[0]=='service':
		pass
	elif component_id_list[0]=='node':
		node_id = component_id_list[1]
		registration_dict[request_msg] = 'node'
		threading.Thread(target=heart_beat_consumer, args=(request_msg,kafka_ip, kafka_port)).start()
		
	else: # component_type[0]=='app'
		app_instance_id = component_id_list[1]
		if (request_msg in registration_dict.keys()):
			pass
		else:
			registration_dict[request_msg] = 'app'
			threading.Thread(target=heart_beat_consumer, args=(request_msg,kafka_ip, kafka_port)).start()
		

def deregister(request_msg):
	print("Deregister request :", request_msg)
	component_id_list = request_msg.split('-', 1)
	if component_id_list[0]=='service':
		pass
	elif component_id_list[0]=='node':
		if request_msg in registration_dict.keys():
			node_id = component_id_list[1]
			registration_dict.pop(request_msg)
	else: # component_type[0]=='app'
		if request_msg in registration_dict.keys():
			app_instance_id = component_id_list[1]
			registration_dict.pop(request_msg)


def get_kafka_service_details(kafka_file_path):
	f = open (kafka_file_path, "r")
	data = json.loads(f.read())
	# kafka_ip = ""
	# kafka_port = "9092"

	kafka_ip = data['ip']
	kafka_port = data['port']
	return kafka_ip, kafka_port


def inform_fault_tolerance(service_name,kafka_ip, kafka_port):
	topic_name = "monitoring"
	print('----------------------INSIDE inform_fault_tolerance------------------------------')
	# producer = KafkaProducer(bootstrap_servers = [':9092'], api_version = (0,10,1))
	producer = KafkaProducer(bootstrap_servers = ['{}:{}'.format(kafka_ip, kafka_port)], api_version = (0,10,1))

	# print("Topic name and service_name:",topic_name, " ", service_name)
	producer.send(topic_name, json.dumps(service_name).encode('utf-8'))

def heart_beat_consumer(service_name,kafka_ip, kafka_port):
	# print("Inside heart_beat :",service_name)
	# print("service names", service_name, kafka_port, kafka_ip)
	while(True):
		# consumer = KafkaConsumer(service_name, bootstrap_servers = [':9092'], api_version = (0,10),consumer_timeout_ms = 5000)
		component_id_list = service_name.split('-', 1)
		if component_id_list[0] == 'node':
			consumer = KafkaConsumer(service_name, bootstrap_servers = ['{}:{}'.format(kafka_ip, kafka_port)], api_version = (0,10),consumer_timeout_ms = 12000)
		else:
			consumer = KafkaConsumer(service_name, bootstrap_servers = ['{}:{}'.format(kafka_ip, kafka_port)], api_version = (0,10),consumer_timeout_ms = 16000)
		for message in consumer:
			pass
		
		if component_id_list[0] != 'service':
			if service_name not in registration_dict.keys():
				break

		print('{} Inactive'.format(service_name))
		inform_fault_tolerance(service_name, kafka_ip, kafka_port)
		time.sleep(20)

def receive_reg_dereg_request(kafka_ip, kafka_port):
	reg_dereg_topic = 'register_deregister'
	while True:
		reg_dereg_consumer = KafkaConsumer(reg_dereg_topic, bootstrap_servers = ['{}:{}'.format(kafka_ip, kafka_port)], api_version = (0,10))
		for message in reg_dereg_consumer:
			message = json.loads(message.value)
			m_list = message.split(' ')			# message = 'register node-ip_9200'
			print('message list format' ,m_list)
			request_type = m_list[0]			# request_type = 'register'
			request_msg = m_list[1]				# request_msg = 'node-ip_9200'
			
			if request_type == 'register':
				register(request_msg)
			else:	# request_type == 'deregister':
				deregister(request_msg)
		
if __name__ == "__main__":

	kafka_file_path = "./configuration/kafka_config.json"
	platform_services_topics = []
	kafka_ip, kafka_port = get_kafka_service_details(kafka_file_path)
	threading.Thread(target=receive_reg_dereg_request, args=(kafka_ip, kafka_port)).start()
	with open('service_names.txt','r') as fp1:
		data = fp1.readlines()
		for line in data:
			word = line.split()
			# print(word)
			platform_services_topics.append(word)

	for service_name in platform_services_topics:
		service_name = 'service-' + service_name[0]
		print('Service name: ', service_name)
		threading.Thread(target=heart_beat_consumer, args=(service_name,kafka_ip, kafka_port)).start()
