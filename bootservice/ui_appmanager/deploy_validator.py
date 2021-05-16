from zipfile import ZipFile
import json
import glob
import uuid
import os
import shutil
import mysql.connector
import ast
from kafka import KafkaProducer
import json


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

    # filepath = "configuration/kafka_config.json"
    # kafka_ip, kafka_port = read_json_kafka(filepath)

    # '{}:{}'.format(kafka_ip,kafka_port)

def insertdata(tablename, data_hdr, data):
    
    
    # def db_connection(filepath):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    hdr_str = ", ".join(i for i in data_hdr)
    sql = "INSERT INTO "+tablename+" ("+hdr_str+") VALUES ("+str(data)[1:-1]+")"
    mycursor.execute(sql)
    
    mydb.commit()


def getallappid():

    
    # def db_connection(filepath):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    sql = "SELECT id FROM apps"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    sensortypeset = set()
    for i in myresult:
        sensortypeset.add(i[0])

    return sensortypeset

def getsensortype(appid):
    
    # def db_connection(filepath):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    sql = "SELECT sensortype FROM apps where id='"+appid+"'"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    sensortypelist = ast.literal_eval(myresult[0][0])
    return sensortypelist


def getcontrollertype(appid):
    
    # def db_connection(filepath):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    sql = "SELECT controllertype FROM apps where id='"+appid+"'"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    controllertypelist = ast.literal_eval(myresult[0][0])
    return controllertypelist

def getallsensortypeuuid(sensor_type):
    # sensortypes

    
    # def db_connection(filepath):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    sql = "SELECT sensor_type_id FROM sensortypes where sensor_type='"+sensor_type+"'"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult[0][0]


def getallcontrollertypeuuid(controller_type):
    # controllertypes

    
    # def db_connection(filepath):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    sql = "SELECT controller_type_id FROM controllertypes where controller_type='"+controller_type+"'"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult[0][0]


def getsensorinstaceid(sentype, locroom,lochouse,locstreet,loccity,alerdytaken):
    sentypeuuid = getallsensortypeuuid(sentype)
    
    
    # def db_connection(filepath):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    wherequery = "sensor_type_id='"+sentypeuuid+"' and loc_room="+str(locroom)+" and loc_house="+str(lochouse)+" and loc_street='"+locstreet+"' and loc_city='"+loccity+"'"
    # return False, wherequery

    # mycursor = mydb.cursor()
    sql = "SELECT id FROM sensorinstance where "+wherequery

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    idlist = []
    for i in myresult:
        idlist.append(i[0])

    for i in idlist:
        if i not in alerdytaken:
            return True, i
    
    return False, "No enough Sesnor Exist"


def getcontrollerinstaceid(sentype, locroom,lochouse,locstreet,loccity,alerdytaken):
    sentypeuuid = getallcontrollertypeuuid(sentype)
    
    
    # def db_connection(filepath):
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    wherequery = "controller_type_id='"+sentypeuuid+"' and loc_room="+str(locroom)+" and loc_house="+str(lochouse)+" and loc_street='"+locstreet+"' and loc_city='"+loccity+"'"
    # return False, wherequery

    # mycursor = mydb.cursor()
    sql = "SELECT id FROM controllerinstance where "+wherequery

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    idlist = []
    for i in myresult:
        idlist.append(i[0])

    for i in idlist:
        if i not in alerdytaken:
            return True, i
    
    return False, -1


def deploy_validator(deploy_data):

    filepathkafka = "configuration/kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    producer = KafkaProducer(bootstrap_servers=['{}:{}'.format(kafka_ip,kafka_port)],api_version=(0,10,1))

    username = deploy_data[0]
    appid = deploy_data[1]
    stime = deploy_data[2]
    duration = deploy_data[3]
    locroom = int(deploy_data[4])
    lochouse = int(deploy_data[5])
    locstreet = deploy_data[6]
    loccity = deploy_data[7]
    repeatation = deploy_data[8]
    intervaltime = deploy_data[9]
    sdate = deploy_data[10]

    try:
        algonum = int(deploy_data[11])
    except Exception:
        algonum = 0


    if appid not in getallappid():
        return "Invalid app id"

    uuidstr = str(uuid.uuid4())
    uuidstr = ''.join(e for e in uuidstr if e != '-')

    #######################
    appinstanceid = "app_instance_"+uuidstr

    sensortypelist = getsensortype(appid)

    sensorinstancelist = [appinstanceid]
    alerdytaken=set()


    for sentype in sensortypelist:
        flag, returnid = getsensorinstaceid(sentype, locroom,lochouse,locstreet,loccity, alerdytaken)

        if flag == False:
            templist = [returnid]
            return "not enough sensor instance  -->  "+ str(returnid)

        alerdytaken.add(returnid)
        sensorinstancelist.append(returnid)

    colscount = len(sensortypelist)
 
    l = ['instaceid']
    for i in range(colscount):
        l.append("index_"+str(i))

    ################################################# DATABASE

    # app table
    insertdata(appid, l, sensorinstancelist)

    ###############################
    appinstanceid = "app_instance_"+uuidstr

    controllertypelist = getcontrollertype(appid)

    controllerinstancelist = [appinstanceid]
    alerdytaken=set()


    for sentype in controllertypelist:
        flag, returnid = getcontrollerinstaceid(sentype, locroom,lochouse,locstreet,loccity, alerdytaken)

        if flag == False:
            templist = [returnid]
            return "not enough controller instance  -->  "+ str(returnid)

        alerdytaken.add(returnid)
        controllerinstancelist.append(returnid)

    colscount = len(controllertypelist)
 
    l = ['instaceid']
    for i in range(colscount):
        l.append("index_"+str(i))

    
    ################################################# DATABASE

    # app table
    insertdata(appid+"_controller", l, controllerinstancelist)

    # deploy-table
    insertdata('deploy', ['appinstanceid','username','appid','sdate','stime','duration','repeatation', 'intervaltime', 'algonum'], [appinstanceid,username,appid,sdate,stime,duration,repeatation,intervaltime, algonum])


    ################################################  KAFKA

    send_str = "start:"+appinstanceid
    producer.send("appmanager_schedular",send_str.encode())

    return "App Deploment started"