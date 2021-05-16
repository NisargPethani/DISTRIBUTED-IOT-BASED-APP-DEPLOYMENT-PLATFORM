import socket
import threading
import sys
import mysql.connector
from kafka import KafkaProducer
from time import sleep
import json
from datetime import datetime
import json

def read_json(filepath):
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

    # filepathkafka = "kafka_config.json"
    # kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    # '{}:{}'.format(kafka_ip,kafka_port)

def getappnameandusername(appinstanceid):
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

    # mycursor = mydb.cursor()

    sql = "SELECT username, appid FROM deploy where appinstanceid='"+appinstanceid+"'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    
    username = myresult[0][0]
    appid = myresult[0][1]

    sql = "SELECT name FROM apps where id='"+appid+"'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    
    appname = myresult[0][0]

    return username, appname

def send_notification(notif_message):

    app_id = sys.argv[1]
    username, appname = getappnameandusername(app_id)           
    #serstr = [appname, username]
    #userstr = str(userstr)
    notif_message = appname + ":" + " " + notif_message   

    filepathkafka = "kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    # '{}:{}'.format(kafka_ip,kafka_port)
    producer = KafkaProducer(bootstrap_servers = ['{}:{}'.format(kafka_ip,kafka_port)], api_version = (0,10,1))

    # topic name is youtube
    producer.send(username,json.dumps(notif_message).encode('utf-8'))
    
    
  



