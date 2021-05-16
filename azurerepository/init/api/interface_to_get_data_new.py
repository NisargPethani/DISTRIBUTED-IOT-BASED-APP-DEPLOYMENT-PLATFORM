from kafka import KafkaConsumer
from json import loads
import ast
import json
import mysql.connector
import json

# FAN_1

# we need to resolve FAN-1

# rosolve hoka repository ma stored ha.
#app_id then only mappint



def read_json_kafka(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    ip = data["ip"]
    port = data["port"]

    return ip, port

    # filepathkafka = "kafka_config.json"
    # kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    # '{}:{}'.format(kafka_ip,kafka_port)

def subscribe_topic(topic_name):

    filepathkafka = "kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    # '{}:{}'.format(kafka_ip,kafka_port)

    consumer = KafkaConsumer(topic_name, 
                        bootstrap_servers = ['{}:{}'.format(kafka_ip,kafka_port)], 
                        api_version = (0,10)
                        #,consumer_timeout_ms = 1000)
                        )
    return consumer
                    

def read_json(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]
    return host_name, user_name, password, database_name


def sensor_idx_to_id_map(index, app_instance_id):
    
    # def db_connection(filepath):
    filepathdb = "db_config.json"
    host_name, user_name, password, database_name = read_json(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    sql = "SELECT appid FROM deploy where appinstanceid='"+app_instance_id+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    appid = myresult[0][0]
    sql = "SELECT index_"+str(index)+" From "+appid+" where instaceid='"+app_instance_id+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sensorid = myresult[0][0]
    return sensorid
	

def get_sensor_data(sensor_idx, app_id):
    sensor_id = sensor_idx_to_id_map(sensor_idx, app_id)
    topic_name = sensor_id
    consumer = subscribe_topic(topic_name)
    # print(consumer)
    for message in consumer:
        sensor_data = message.value.decode()

        sensor_data = ast.literal_eval(sensor_data)
        # print(sensor_data)
        return sensor_data

def get_stream_data(sensor_idx, app_id, number_of_data_points):
    sensor_id = sensor_idx_to_id_map(sensor_idx, app_id)
    topic_name = sensor_id
    consumer = subscribe_topic(topic_name)
    sensor_data_list = []
    i=0
    for message in consumer:
        if(i==number_of_data_points):
            break
        sensor_data = ast.literal_eval(sensor_data)
        sensor_data = message.value
        sensor_data_list.append(sensor_data)
        # print(sensor_data)
        i+=1

    return sensor_data_list
    
    
    


