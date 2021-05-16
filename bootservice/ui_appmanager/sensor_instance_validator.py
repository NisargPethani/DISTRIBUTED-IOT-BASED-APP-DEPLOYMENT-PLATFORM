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

    # filepathkafka = "configuration/kafka_config.json"
    # kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    # '{}:{}'.format(kafka_ip,kafka_port)
    
def getallsensortype():
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
    sql = "SELECT sensor_type FROM sensortypes"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    sensortypeset = set()
    for i in myresult:
        sensortypeset.add(i[0])

    return sensortypeset


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

def sensor_instance_validator(filepath):
    return_str = ""


    filepathkafka = "configuration/kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    print()   
    print()   
    print()   
    print("#############################")
    print('{}:{}'.format(kafka_ip,kafka_port))
    print("#############################")
    print()   
    print()   
    print()   
 
    producer = KafkaProducer(bootstrap_servers=['{}:{}'.format(kafka_ip,kafka_port)],api_version=(0,10,1))
    
    with ZipFile(filepath, 'r') as zip:

        dir_path = filepath[:-4]

        zip.printdir()
        print('Extracting all the files now...')
        zip.extractall(dir_path)

        all_files = glob.glob(dir_path+"/*")
        file_list = glob.glob(dir_path+"/*.json")

        final_flag=True
        if(len(all_files) != len(file_list) or len(all_files)<=0):
            final_flag = False
            return_str = "Wrong Directory Structue OR Unnecessory file/files have found in zip"

        if final_flag == True:

            for file in file_list:

                uuidstr = str(uuid.uuid4())
                uuidstr = ''.join(e for e in uuidstr if e != '-')
                new_name = dir_path+"/sensor_instance_" + uuidstr + ".json"

                os.rename(file, new_name)

            file_list = glob.glob(dir_path+"/*.json")

            for file1 in file_list:

                with open(file1,"r") as file:
                    content = file.read()
                    sensor_instance_dict = json.loads(content)
                    keys = sensor_instance_dict.keys()

                    if(("sensor_type" in keys) and ("sensor_location") in keys and "geo_location" in keys):

                        sensor_location_keys = sensor_instance_dict["sensor_location"].keys()
                        geo_location_keys = sensor_instance_dict["geo_location"].keys()
                        sensor_location = sensor_instance_dict["sensor_location"]
                        geo_location = sensor_instance_dict["geo_location"]

                        if(("ip" in sensor_location_keys) and ("port" in sensor_location_keys)):
                            ip = sensor_location["ip"]
                            port = sensor_location["port"]

                            matched = re.match("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", ip)
                            is_ip = bool(matched)
                            if is_ip == False:
                                final_flag = False
                                return_str = "Invalid ip address is defined in 'sensor_location' -> 'ip' field... Defined ip: '"+ip+"' "
                                break

                            try: 
                                port = int(port)
                            except ValueError:
                                final_flag = False
                                return_str = "Invalid port is defined in 'sensor_location' -> 'port' field.. Defined port: "+str([port])+" "
                                break

                        else:
                            final_flag = False
                            return_str = "one of ['ip', 'port'] is missing in 'sensor_location' field in one of files"
                            break

                        if(("room_no" in geo_location_keys) and ("house_no" in geo_location_keys) and ("street" in geo_location_keys) and ("city" in geo_location_keys)):
                            if((not(geo_location["room_no"].isnumeric())) or (not(geo_location["house_no"].isnumeric()))):
                                final_flag = False
                                return_str = "Invalid house_no/ room_no is defined in 'geo_location' field.. Defined values house_no: "+str([geo_location["house_no"]])+" room_no: "+str([geo_location["room_no"]])+" "
                                break
                                #print("CASE4")
                        else:
                            final_flag = False
                            return_str = "one of ['room_no', 'house_no', 'street', 'city'] is missing in 'geo_location' field in one of files"
                            break

                    else:
                        final_flag = False
                        return_str = "one of ['sensor_type', 'sensor_location', 'geo_location'] is missing in one of files"
                        break
    
        valid_flag = final_flag

        if final_flag == True:
            source_dir = dir_path     
            file_names = os.listdir(source_dir)

            allsensortypes = getallsensortype()

            for file_name in file_names:
                file_path = os.path.join(source_dir, file_name)

                with open(file_path,"r") as file:
                    
                    content = file.read()                    
                    sensor_instance_dict = json.loads(content)
                    
                    ######### File extracting

                    sensor_type = sensor_instance_dict['sensor_type']

                    if sensor_type not in allsensortypes:
                        return_msg = [False, "Sensor type yet not exist"]
                        return_msg = str(return_msg)

                        return return_msg 

            ############################################## DATABASE

            source_dir = dir_path                
            file_names = os.listdir(source_dir)
                
            for file_name in file_names:
                file_path = os.path.join(source_dir, file_name)

                with open(file_path,"r") as file:
                    
                    content = file.read()                    
                    sensor_instance_dict = json.loads(content)
                    
                    ######### File extracting

                    id = file_name[:-5]
                    sensor_type = sensor_instance_dict['sensor_type']
                    sensor_type_id = getallsensortypeuuid(sensor_type)

                    ip = sensor_instance_dict['sensor_location']['ip']
                    port = int(sensor_instance_dict['sensor_location']['port'])

                    loc_room = int(sensor_instance_dict['geo_location']['room_no'])
                    loc_house = int(sensor_instance_dict['geo_location']['house_no'])
                    loc_street = sensor_instance_dict['geo_location']['street']
                    loc_city = sensor_instance_dict['geo_location']['city']

                    insertdata('sensorinstance', ['id', 'sensor_type_id', 'ip', 'port', 'loc_room', 'loc_house', 'loc_street', 'loc_city'], [id, sensor_type_id, ip, port, loc_room, loc_house, loc_street, loc_city])
                    insertdata('sensorinstanceipport', ['ip', 'port', 'id'], [ip, port, id])

                    # id
                    producer.send("appmanager_sensormanager", id.encode())

            ############################################## Move
            source_dir = dir_path
            target_dir = "repository/sensor_instance_info"
                
            file_names = os.listdir(source_dir)
                
            for file_name in file_names:
                shutil.move(os.path.join(source_dir, file_name), target_dir)

            shutil.rmtree("temp/")
            
            return_str = "All validation has been done + All things has been saved in database"
            return [True, return_str]
        else:
            return [False, return_str]