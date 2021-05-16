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


def sensor_type_validator(filepath):
    return_str = ""
    
    with ZipFile(filepath, 'r') as zip:


        dir_path = filepath[:-4]

        zip.printdir()
        print('Extracting all the files now...')
        zip.extractall(dir_path)


        types = ["float","int","string"]
        
        file_list = glob.glob(dir_path+"/*.json")
        all_files = glob.glob(dir_path+"/*.*")
        
        list_flags=[]

        final_flag=True
        if(len(all_files) != len(file_list) or len(all_files)<=0):
            final_flag = False
            return_str = "Wrong Directory Structue OR Unnecessory file/files have found in zip"

        if final_flag == True:
            for file in file_list:

                file_obj = open(file, 'r')
                content = file_obj.read()                    
                sensor_instance_dict = json.loads(content)

                sensor_instance_dict['sensor_type'] = file.split("/")[-1][:-5]
                
                json_object = json.dumps(sensor_instance_dict, indent = 4)

                uuidstr = str(uuid.uuid4())
                uuidstr = ''.join(e for e in uuidstr if e != '-')

                file_new_name = "sensor_type_" + uuidstr + ".json"

                with open(dir_path+"/"+file_new_name, "w") as outfile:
                    outfile.write(json_object)

                os.remove(file)

            file_list = glob.glob(dir_path+"/*.json")
            print(file_list)

            for j in file_list:
                with open(str(j),'r') as f:
                    data = json.load(f)
                    if "company" not in data or "model" not in data or "data_rate" not in data or "field_count" not in data:
                        final_flag = False
                        return_str = "one of ['model', 'company', 'data_rate', 'field_count'] is missing in one of files"
                        break

                    if data["sensor_type"] in getallsensortype():
                        final_flag = False
                        return_str = "Invalid Sensor type... Sensor Type: "+str([data["sensor_type"]])+" already exist"
                        break

                    try: 
                        index = int(data["field_count"])
                        for i in range(1,index+1):
                            field_name ="field_"+str(i)
                            if field_name not in data or data[field_name] not in types:
                                final_flag = False
                                return_str = "Not sufficient fields information/ Invalid data-type of field... Supported types: "+str(types)
                                break
                    except ValueError:
                        final_flag = False
                        return_str = "Invalid field count is defined.. Defined field count: "+str([data["field_count"]])+" "
                        break                        
                                        
        valid_flag = final_flag
        
        if valid_flag == True:
            ############################################## DATABASE

            source_dir = dir_path                
            file_names = os.listdir(source_dir)
                
            for file_name in file_names:
                file_path = os.path.join(source_dir, file_name)

                with open(file_path,"r") as file:
                    
                    content = file.read()                    
                    sensor_instance_dict = json.loads(content)
                    
                    sensor_type_id = file_name.split("/")[-1][:-5]

                    sensor_type = sensor_instance_dict['sensor_type']
                    fieldcount  = int(sensor_instance_dict['field_count'])
                    fields  = []
                    datarate  = sensor_instance_dict['data_rate']
                    company  = sensor_instance_dict['company']
                    model  = sensor_instance_dict['model']

                    for i in range(1,fieldcount+1):
                        field_name ="field_"+str(i)
                        fields.append(sensor_instance_dict[field_name])

                    fields = str(fields)

                    insertdata('sensortypes', ['sensor_type_id', 'sensor_type','fieldcount', 'fields', 'datarate', 'company', 'model'], [sensor_type_id, sensor_type,fieldcount, fields, datarate, company, model])

            ############################################## Move
            source_dir = dir_path
            target_dir = "repository/sensor_type_info"
                
            file_names = os.listdir(source_dir)
                
            for file_name in file_names:
                shutil.move(os.path.join(source_dir, file_name), target_dir)

            shutil.rmtree("temp/")
            
            return_str = "All validation has been done + All things has been saved in database"
            return [True, return_str]
        else:
            return [False, return_str]