from zipfile import ZipFile
import json
import glob
import uuid
import os
import shutil
import mysql.connector
import json
import upload_app_to_repo

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



def createtable(tablename, colscount):

    # tablename = ''.join(e for e in tablename if e != '-')
    
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

    l = []
    for i in range(colscount):
        l.append("index_"+str(i)+" VARCHAR(255)")

    lstr = ", ".join(i for i in l)

    sql = "CREATE TABLE "+tablename+ " (instaceid VARCHAR(255),"+lstr+")"
    print(sql)
    mycursor.execute(sql)


def createtablecontroller(tablename, colscount):

    # tablename = ''.join(e for e in tablename if e != '-')
    
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

    l = []
    for i in range(colscount):
        l.append("index_"+str(i)+" VARCHAR(255)")

    lstr = ", ".join(i for i in l)

    sql = "CREATE TABLE "+tablename+ "_controller (instaceid VARCHAR(255),"+lstr+")"
    print(sql)
    mycursor.execute(sql)

def app_validator(filepath):

    return_str = ""    
    
    try:
        shutil.rmtree("temp/App/")
    except Exception:
        pass

    os.mkdir("temp/App")
    ############################################################

    with ZipFile(filepath, 'r') as zip:
        zip.printdir()
        zip.extractall("temp/App")

    ####################################################################
    allsensortypes = getallsensortype()
    allcontrollertypes = getallcontrollertype()

    file_list = glob.glob("temp/App/*")
    final_flag = True

    if len(file_list)!=2 or "temp/App/scripts" not in file_list or "temp/App/configuration" not in file_list:
        final_flag = False
    else:
        file_list1 = glob.glob("temp/App/configuration/*.json")
        total_file1 = glob.glob("temp/App/configuration/*.*")
        if 'temp/App/configuration/appname.json' in file_list1 and 'temp/App/configuration/sensor.json' in file_list1 and 'temp/App/configuration/controller.json' in file_list1 :
            with open("temp/App/configuration/appname.json",'r') as f:
                data = json.load(f)
                if "app_name" not in data:
                    final_flag = False
            with open("temp/App/configuration/sensor.json",'r') as f:
                data = json.load(f)
                if "sensor_instance_count" in data and isinstance(data["sensor_instance_count"], int) and "sensor_instance_info" in data:
                    index = data["sensor_instance_count"]
                    if index == len(data["sensor_instance_info"]):
                        for idx, i in enumerate(data["sensor_instance_info"]):
                            if i["sensor_instance_index"] != idx:
                                final_flag = False
                                break
                            if i['sensor_instance_type'] not in allsensortypes:
                                return_str = "Sensor type yet not exist"
                                # return_msg = str(return_msg)

                                return [False, return_str]
                    else:
                        final_flag = False
                else:
                    final_flag=False

            with open("temp/App/configuration/controller.json",'r') as f:
                data = json.load(f)
                print("*********************************************")
                print(data)
                print("*********************************************")
                if "controller_instance_count" in data and isinstance(data["controller_instance_count"], int) and "controller_instance_info" in data:
                    index = data["controller_instance_count"]
                    if index == len(data["controller_instance_info"]):
                        for idx, i in enumerate(data["controller_instance_info"]):
                            if i["controller_instance_index"] != idx:
                                final_flag = False
                                break
                            if i['controller_instance_type'] not in allcontrollertypes:
                                return_str = "controller type yet not exist"
                                # return_msg = str(return_msg)

                                return [False, return_str]
                    else:
                        final_flag = False
                else:
                    final_flag=False
        else:
            final_flag=False
    
    # return final_flag
            
    if final_flag == True:

        ############################################## name change

        uuidstr = str(uuid.uuid4())
        uuidstr = ''.join(e for e in uuidstr if e != '-')

        new_dir_name = "temp/app_"+ uuidstr
        os.rename("temp/App", new_dir_name)

        ############################################## DATABASE
        
        appname_json_path = os.path.join(new_dir_name, 'configuration', 'appname.json')
        sensor_json_path = os.path.join(new_dir_name, 'configuration', 'sensor.json')    
        controller_json_path = os.path.join(new_dir_name, 'configuration', 'controller.json')        

        # id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), sensorcount int, sensortype VARCHAR(1023)

        appname_json_dict = json.load(open(appname_json_path, 'r'))
        sensor_json_dict = json.load(open(sensor_json_path, 'r'))
        controller_json_dict = json.load(open(controller_json_path, 'r'))


        app_uuid = new_dir_name.split("/")[-1]
        name = appname_json_dict['app_name']

        #########################
        sensorcount= int(sensor_json_dict['sensor_instance_count'])

        sensortype = []
        for i in sensor_json_dict['sensor_instance_info']:
            sensortype.append(i['sensor_instance_type'])

        sensortypestr = str(sensortype)

        # insertdata('apps', ['id', 'name', 'sensorcount', 'sensortype'],[app_uuid, name, sensorcount, sensortypestr])
        createtable(app_uuid, sensorcount)  

        ##########################
        controllercount= int(controller_json_dict['controller_instance_count'])

        controllertype = []
        for i in controller_json_dict['controller_instance_info']:
            controllertype.append(i['controller_instance_type'])

        controllertypestr = str(controllertype)

        insertdata('apps', ['id', 'name', 'sensorcount', 'sensortype', 'controllercount', 'controllertype'],[app_uuid, name, sensorcount, sensortypestr, controllercount, controllertypestr])      
        createtablecontroller(app_uuid, controllercount)

        ############################################## Move
        source_dir = new_dir_name
        target_dir = "repository/apps_info"
            
        shutil.move(source_dir, target_dir)

        des_dir = os.path.join(target_dir, app_uuid, 'scripts')

        # shutil.copy('application_helper/interface_to_get_data_new.py', des_dir)
        # shutil.copy('application_helper/action_and_notification_api.py', des_dir)
        # shutil.copy('application_helper/docker_file_generator.py', des_dir)
        # shutil.copy('application_helper/platform_requirements.txt', des_dir)
        # shutil.copy('application_helper/start.sh', des_dir)
        # shutil.copy('application_helper/db_config.json', des_dir)

        print("Uploading App....")
        upload_app_to_repo.upload_app(app_uuid)

        shutil.rmtree("temp/")
        
        return_str = "Successful"    
        return [True, return_str]
    else:
        return_str = "Fail"    
        return [False, return_str]
