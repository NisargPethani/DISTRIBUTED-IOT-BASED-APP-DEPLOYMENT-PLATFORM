import sys
from kafka import KafkaProducer
from time import sleep
import json
import time
from datetime import datetime
import threading
from requests import get
import json

kafka_config_filepath = "kafka_config.json"

def get_kafka_service_details(kafka_config_filepath):
    f = open (kafka_config_filepath, "r")
    data = json.loads(f.read())

    kafka_ip = data["ip"]
    kafka_port = data["port"]

    return kafka_ip, kafka_port


def register_deregister_to_heart_beat_manager(request_type): 
    print("----------------Registration with Heart Beat Manager---------------------")
    kafka_ip, kafka_port = get_kafka_service_details(kafka_config_filepath)

    topic_name = "register_deregister"
    name_type = sys.argv[0].split(".",1)[0]
 
    if name_type == "node2" or name_type == "node":
        message = "{} {}-{}_{}".format(request_type, "node", get('https://api.ipify.org').text, "8004") 
        print("Node {} message : {}\n".format(request_type,message))
    else:
        message = "{} {}-{}".format(request_type, "application", sys.argv[1])
        print("Application {} message : {}\n".format(request_type,message))
    
    producer = KafkaProducer(bootstrap_servers = ['{}:{}'.format(kafka_ip, str(kafka_port))], 
                        api_version = (0,10,1))
    
    print("Topic name :",topic_name)
    
    producer.send(topic_name, json.dumps(message).encode('utf-8'))


def heart_beat():
    print("----------------- Heart Beat Started -------------------------")

    kafka_ip, kafka_port = get_kafka_service_details(kafka_config_filepath)

    topic_name = sys.argv[0].split(".",1)[0]

    if topic_name == "node2" or topic_name == "node":
        topic_name = "{}-{}_{}".format("node",get('https://api.ipify.org').text, "8004")
        # message = "{} {}_{}:{}".format(request_type, "node", get('https://api.ipify.org').text, "8004") 
        # print("Node {} message : {}\n".format(request_type,message))
    elif "application" in topic_name:
        topic_name = "{}-{}".format("application", sys.argv[1])
        # message = "{} {}_{}".format(request_type, "application", sys.argv[1])
        # print("Application {} message : {}\n".format(request_type,message))
    else:
        topic_name = "{}-{}".format("service", topic_name)
    
    print("Topic Name :", topic_name)

    producer = KafkaProducer(bootstrap_servers = ['{}:{}'.format(kafka_ip, str(kafka_port))], 
                        api_version = (0,10,1))
    while True:
        producer.send(topic_name, json.dumps("1").encode('utf-8'))
        #print("Message sent :", 1)
        time.sleep(5)

def start_heart_beat():
    name_type = sys.argv[0].split(".",1)[0]
    if name_type == "node2" or name_type == "node" or "application" in name_type:
        register_deregister_to_heart_beat_manager("register")
    
    thread = threading.Thread(target=heart_beat)
    thread.start()

