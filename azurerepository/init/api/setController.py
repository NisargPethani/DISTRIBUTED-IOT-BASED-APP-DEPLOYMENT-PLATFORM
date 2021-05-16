from kafka import KafkaProducer
from json import loads
import ast
import json
import mysql.connector


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
    


def subscribe_topic(topic_name):
    
    return producer
                    

def controller_idx_to_id_map(index, app_instance_id):
    # nisarg k bharose...
    filepathdb = "db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)

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
    sql = "SELECT index_"+str(index)+" From "+appid+"_controller where instaceid='"+app_instance_id+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    controllerid = myresult[0][0]

    return controllerid

def set_controller_data(controller_idx, data, app_id):

    # print("\t **** Req for set controller data: ", controller_idx, data, app_id)
    controller_id = controller_idx_to_id_map(controller_idx, app_id)

    # print("\t **** cntroller id", controller_id)

    topic_name = controller_id
    message_to_controller = data

    # print("\t **** Making Producer")


    filepathkafka = "kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepathkafka)
    producer = KafkaProducer(bootstrap_servers = ['{}:{}'.format(kafka_ip,kafka_port)], api_version = (0,10))

    # print("\t **** Data sending on kafka topic:", topic_name)

    producer.send(topic_name, data.encode('utf-8'))

    # print("\t **** Data sent")
        
# later version....

# def set_controller_data(controller_idx, controller_function, data, app_id):
#     controller_id = controller_idx_to_id_map(controller_idx, app_id)
#     topic_name = controller_id
#     message_to_controller = {controller_function:data}  #dictionary containing controller funcction as key and its data as function
#     producer = subscribe_topic(topic_name)
#     producer.send(topic_name, json.dumps(message_to_controller).encode('utf-8'))







    
    
    


