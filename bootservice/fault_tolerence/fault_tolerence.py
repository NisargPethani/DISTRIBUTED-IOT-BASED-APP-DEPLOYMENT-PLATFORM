import sys
import threading
from kafka import KafkaConsumer, KafkaProducer
from time import sleep
import json
import time
from datetime import datetime
import json
from requests import get
from helper_file import ssh_util
import socket
import os
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



def kafka_producer_fault_tolerance(app_instance_id,kafka_ip,kafka_port):
	topic_name = "restart_app"
	producer = KafkaProducer(bootstrap_servers = ['{}:{}'.format(kafka_ip, kafka_port)], api_version = (0,10,1))
	producer.send(topic_name, json.dumps(app_instance_id).encode('utf-8'))

def get_node_manager_details(service_config_path):
	f = open (service_config_path, "r")
	data = json.loads(f.read())
	node_manager_ip = data['node_manager']['ip']
	#node_manager_port = data['node_manager']['port']
	node_manager_port = 10000
	return node_manager_ip, node_manager_port

def get_service_details(service_config_path, service_name):
	f = open (service_config_path, "r")
	data = json.loads(f.read())
	service_ip = data[service_name]['ip']
	service_username = data[service_name]['username']
	#node_manager_port = data['node_manager']['port']
	#node_manager_port = 10000
	return service_ip,service_username

def node_manager_client_connect(node_ip,node_port,service_config_path):
	node_manager_ip, node_manager_port = get_node_manager_details(service_config_path)

	try:
		sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
	except socket.error as error:
		print("Socket creation failed with error :", error)
		sys.exit(0)

	connected = False
	while(not connected):
		try:
			sockt.connect((node_manager_ip, node_manager_port))
			request = "{} {} {}".format("fault_tolerance",node_ip, node_port)
			print(request)
			sockt.sendall(request.encode()) 
			connected = True
		except socket.error as error:
			print("client:",error)
			connected = True

	print("Connected Successfully!!")
	sockt.close()


def get_type(topic_name):
	topic_type = (topic_name.split("-",1))[0]
	print("Type : ",topic_type )
	return topic_type 

def get_kafka_service_details(kafka_filepath):
	f = open (kafka_filepath, "r")
	# Reading from file
	data = json.loads(f.read())

	# kafka_ip = ""
	# kafka_port = "9092"
	kafka_ip = data["ip"]
	kafka_port = data["port"]
	return kafka_ip, kafka_port

def get_service_init_details(service_name):

	node_ip = ""
	node_port = ""
	command_to_init_service = ""
	return node_ip, node_port, command_to_init_service

# def reinit_service(service_name):
# 	node_ip, node_port, command_to_init_services = get_service_init_details(service_name)
# 	## do something to run the service again.
# 	print("Service : {} up inside reinti service!!!".format(service_name))



def fault_monitoring(kafka_ip, kafka_port, service_config_path):
	while(True):
		consumer = KafkaConsumer("monitoring", bootstrap_servers = ['{}:{}'.format(kafka_ip, kafka_port)], api_version = (0,10))
		for message in consumer:
			kafka_topic_name = json.loads(message.value)
			print("Kafka Topic Recieved : ", kafka_topic_name)
			topic_type = get_type(kafka_topic_name)			
			if topic_type == "node":
				print("Topic Type :{}".format(topic_type))
				request = (kafka_topic_name.split('-', 1))
				ip_port = request[1].split("_",1)
				node_ip = ip_port[0]
				node_port = ip_port[1]
				thread = threading.Thread(target=node_manager_client_connect, args=([node_ip,node_port,service_config_path]))
				thread.start()
				
			elif topic_type == "application":
				print("Topic Type :{}".format(topic_type))

				request = (kafka_topic_name.split('-', 1))
				app_instance_id = request[1]
				print("Application Instance ID : ", app_instance_id)

				kafka_producer_fault_tolerance(app_instance_id, kafka_ip, kafka_port)
				
			elif topic_type == "service":
				print("Topic Type :{}".format(topic_type))
				request = (kafka_topic_name.split('-', 1))
				service_name = request[1]
				print("Service Name :", service_name)

				ssh_object = ssh_util()

				command = "sudo docker start container_{}".format(service_name)
				commands = [command]
				vm_ip, vm_username = get_service_details(service_config_path, service_name)

				flag, ssh_output = ssh_object.execute_command(commands, vm_ip, vm_username)
				print("SSH Output :", ssh_output)
				if (flag):
					print("---------------Service Restarted Successfully")
				else:
					print("--------------Ooops!!!! Service not restart-----------------")

			# threading.Thread(target=reinit_service, args=([kafka_topic_name])).start()







if __name__ == "__main__":
	kafka_filepath = "configuration/kafka_config.json"
	service_config_path = "configuration/services_config.json"
	# platform_services_topics = []

	# with open('service_names.txt','r') as fp1:
	# 	data = fp1.readlines()
	# 	for line in data:
	# 		word = line.split()
	# 		# print(word)
	# 		platform_services_topics.append(word)
	kafka_ip, kafka_port = get_kafka_service_details(kafka_filepath)
	fault_monitoring(kafka_ip, kafka_port, service_config_path)
	# for service_name in platform_services_topics:
	# 	threading.Thread(target=heart_beat_consumer, args=(kafka_ip, kafka_port)).start()

	
