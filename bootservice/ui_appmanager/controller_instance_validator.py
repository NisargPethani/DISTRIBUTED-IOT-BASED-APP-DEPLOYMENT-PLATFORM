from zipfile import ZipFile
import json
import glob
import uuid
import os
import shutil
import mysql.connector
from kafka import KafkaProducer
import re
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

def getallcontrollertype():
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
    sql = "SELECT controller_type FROM controllertypes"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    controllertypeset = set()
    for i in myresult:
        controllertypeset.add(i[0])

    return controllertypeset


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

def controller_instance_validator(filepath):

    filepathkafka = "configuration/kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    return_str = ""    
    producer = KafkaProducer(bootstrap_servers=['{}:{}'.format(kafka_ip,kafka_port)],api_version=(0,10,1))
    
    with ZipFile(filepath, 'r') as zip:

        folder_name = "temp"
        
        file_name = filepath.split("/")[-1]
        file_name_without_ext = file_name[:-4]

        with ZipFile(os.path.join(folder_name, file_name), 'r') as zip:
            #zip.printdir()
            zip.extractall(folder_name)

        final_flag = True

        file_list = glob.glob(folder_name+"/*.json")
        all_files = glob.glob(folder_name+"/*")

        final_flag=True
        if(len(all_files)-1 != len(file_list) or len(all_files)-1<=0):
            final_flag = False
            return_str = "Wrong Directory Structue OR Unnecessory file/files have found in zip"

        if final_flag == True:

            for file in file_list:

                uuidstr = str(uuid.uuid4())
                uuidstr = ''.join(e for e in uuidstr if e != '-')
                new_name = "controller_instance_" + uuidstr + ".json"

                os.rename(file, os.path.join(folder_name,new_name))

            file_list = glob.glob(folder_name+"/*.json")

            #print(file_list)
            
            if len(file_list)==0:
                final_flag = False
                return_str = "No files in zip/ Wrong directory structure... (Select all configuration and compress it and upload zip file)"
            else:
                final_flag = True
                for i in file_list:
                    with open(i,'r') as f:
                        data = json.load(f)
                        controller_type_set = getallcontrollertype()

                        if "controller_type" not in data or "controller_location" not in data or "geo_location" not in data:
                            final_flag = False
                            return_str = "one of ['controller_type', 'controller_location', 'geo_location'] is missing in one of the files"
                            break
                        else:
                            if data["controller_type"] not in controller_type_set:
                                final_flag = False
                                return_str = "controller_type:'"+data["controller_type"]+"' is not present on plateform... please upload contoller with one of this: "+str(controller_type_set)
                                break

                            lib1 = data["controller_location"]
                            lib2 = data["geo_location"]
                            if "ip" not in lib1 or "port" not in lib1:
                                final_flag = False
                                return_str = "one of ['ip', 'port'] is missing in 'controller_location' field in one of files"
                                break

                            ip = lib1["ip"]
                            port = lib1["port"]
                            l = len(lib2)
                            matched = re.match("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", ip)
                            is_ip = bool(matched)
                            if is_ip == False or l==0:
                                final_flag = False
                                return_str = "Invalid ip address is defined in 'controller_location' -> 'ip' field... Defined ip: '"+ip+"' "
                                break
                            try: 
                                port = int(port)
                            except ValueError:
                                final_flag = False
                                return_str = "Invalid port is defined in 'controller_location' -> 'port' field.. Defined port: "+str([port])+" "
                                break

                            if "city" not in lib2 or "street" not in lib2 or "house_no" not in lib2 or "room_no" not in lib2:
                                final_flag = False
                                return_str = "one of ['city', 'street', 'house_no', 'room_no'] is missing in 'geo_location' field inone of files"
                                break

                            house_no = lib2["house_no"]
                            room_no = lib2["room_no"]

                            try: 
                                t = int(room_no)
                                t = int(house_no)
                            except ValueError:
                                final_flag = False
                                return_str = "Invalid house_no/ room_no is defined in 'geo_location' field.. Defined values house_no: "+str([house_no])+" room_no: "+str([room_no])+" "
                                break

        valid_flag = final_flag

        if valid_flag == True:
            ############################################## DATABASE
            for i in file_list:
                with open(i,'r') as f:
                    controller_instance_dict = json.load(f)

                    file_name = i.split("/")[-1]

                    ######### File extracting

                    id = file_name[:-5]
                    controller_type = controller_instance_dict['controller_type']
                    controller_type_id = getallcontrollertypeuuid(controller_type)

                    ip = controller_instance_dict['controller_location']['ip']
                    port = int(controller_instance_dict['controller_location']['port'])

                    loc_room = int(controller_instance_dict['geo_location']['room_no'])
                    loc_house = int(controller_instance_dict['geo_location']['house_no'])
                    loc_street = controller_instance_dict['geo_location']['street']
                    loc_city = controller_instance_dict['geo_location']['city']

                    insertdata('controllerinstance', ['id', 'controller_type_id', 'ip', 'port', 'loc_room', 'loc_house', 'loc_street', 'loc_city'], [id, controller_type_id, ip, port, loc_room, loc_house, loc_street, loc_city])
                    insertdata('controllerinstanceipport', ['ip', 'port', 'id'], [ip, port, id])

                    # id
                    producer.send("appmanager_controllerserver", id.encode())

            ############################################## Move
            target_dir = "repository/controller_instance_info"
                
            file_names = os.listdir(folder_name)
                
            for file_name in file_names:
                if file_name[-5:] == ".json":
                    shutil.move(os.path.join(folder_name, file_name), target_dir)

            shutil.rmtree("temp/")            
            
            return_str = "All validation has been done + All things has been saved in database"
            return [True, return_str]
        else:
            return [False, return_str]