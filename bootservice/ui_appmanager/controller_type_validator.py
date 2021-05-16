from zipfile import ZipFile
import json
import glob
import uuid
import os
import shutil
import mysql.connector
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


def controller_type_validator(filepath):

    return_str = ""    
    with ZipFile(filepath, 'r') as zip:

        folder_name = "temp"
        
        file_name = filepath.split("/")[-1]
        file_name_without_ext = file_name[:-4]

        with ZipFile(os.path.join(folder_name,file_name), 'r') as zip:
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

                file_obj = open(file, 'r')
                content = file_obj.read()                    
                controller_instance_dict = json.loads(content)

                controller_instance_dict['controller_type'] = file.split("/")[-1][:-5]
                
                json_object = json.dumps(controller_instance_dict, indent = 4)

                uuidstr = str(uuid.uuid4())
                uuidstr = ''.join(e for e in uuidstr if e != '-')

                file_new_name = "controller_type_" + uuidstr + ".json"

                # Writing to sample.json
                with open(os.path.join(folder_name,file_new_name), "w") as outfile:
                    outfile.write(json_object)

                os.remove(file)
            
            file_list = glob.glob(folder_name+"/*.json")
                    
            valid_datatype = ["string","int","float"]
            final_flag = True
            if len(file_list)==0:
                final_flag = False
                return_str = "No files in zip/ Wrong directory structure... (Select all configuration and compress it and upload zip file)"
            else:
                final_flag = True
                for i in file_list:
                    with open(i,'r') as f:
                        controller_type_dict = json.load(f)
                        #print(data)
                        if "company" not in controller_type_dict or "model" not in controller_type_dict or "input" not in controller_type_dict or controller_type_dict["input"].lower() not in valid_datatype :
                            final_flag = False
                            return_str = "one of ['company', 'model', 'input'] is missing in one of the files"
                            break

                        if controller_type_dict["controller_type"] in getallcontrollertype() :
                            final_flag = False
                            return_str = "Controller Type: '"+controller_type_dict["controller_type"]+"' already exist on plateform"
                            break

        valid_flag = final_flag
        
        if valid_flag == True:

            ############################################## DATABASE
            for i in file_list:
                with open(i,'r') as f:
                    controller_type_dict = json.load(f)
                    
                    company = controller_type_dict["company"]
                    model = controller_type_dict["model"]
                    input_datatype = controller_type_dict["input"]
                    controller_type = controller_type_dict["controller_type"]

                    controller_type_id = i.split("/")[-1][:-5]

                    insertdata('controllertypes', ['controller_type_id','controller_type', 'input', 'company', 'model'], [controller_type_id,controller_type, input_datatype, company, model])

            ############################################## Move
            target_dir = "repository/controller_type_info"
                
            file_names = os.listdir(folder_name)
                
            for file_name in file_names:
                if file_name[-5:] == ".json":
                    shutil.move(os.path.join(folder_name, file_name), target_dir)

            shutil.rmtree("temp/")
            
            return_str = "All validation has been done + All things has been saved in database"
            return [True, return_str]
        else:
            return [False, return_str]