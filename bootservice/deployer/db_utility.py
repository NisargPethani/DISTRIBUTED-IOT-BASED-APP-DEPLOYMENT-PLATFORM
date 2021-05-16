import mysql.connector
import sys
import uuid
import json
  
f = open('configuration/db_config.json',)
db_config = json.load(f)
f.close()

# dep_db = mysql.connector.connect(
#   host=db_config["host"],
#   user=db_config["user"],
#   password=db_config["password"],
#   database="IOT_PLATFORM"
# )

# dep_db_cursor = dep_db.cursor()


def read_json(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]
    return host_name, user_name, password, database_name


def insert_into_db(job_id, app_instance_id, server_address, app_run_type):

    dep_db = mysql.connector.connect(
    host=db_config["host"],
    user=db_config["user"],
    password=db_config["password"],
    database="IOT_PLATFORM"
    )

    dep_db_cursor = dep_db.cursor()

    sql = "SELECT * FROM Deployment_manager_db WHERE App_instance_ID = '{}'".format(app_instance_id)
    value = (app_instance_id)
    dep_db_cursor.execute(sql)
    result = dep_db_cursor.fetchall()

    if len(result) > 0:
        sql = "DELETE FROM Deployment_manager_db WHERE App_instance_ID = '{}'".format(app_instance_id)
        value = (app_instance_id)
        dep_db_cursor.execute(sql)
        dep_db.commit()

    sql = "INSERT INTO Deployment_manager_db VALUES (%s, %s, %s, %s)"
    values = (job_id, app_instance_id, server_address, app_run_type)
    
    print("####################################################################")
    print(values)
    print("####################################################################")

    dep_db_cursor.execute(sql, values)
    dep_db.commit()
    return

def get_server_address(app_instance_id):
    dep_db = mysql.connector.connect(
    host=db_config["host"],
    user=db_config["user"],
    password=db_config["password"],
    database="IOT_PLATFORM"
    )

    dep_db_cursor = dep_db.cursor()

    sql = "SELECT Server_address FROM Deployment_manager_db WHERE App_instance_ID = '{}'".format(app_instance_id)
    value = (app_instance_id)
    dep_db_cursor.execute(sql)
    result = dep_db_cursor.fetchone()

    if result is None:
        return False, None
    else:
        return True, result[0]

def get_app_run_type(app_instance_id):
    dep_db = mysql.connector.connect(
    host=db_config["host"],
    user=db_config["user"],
    password=db_config["password"],
    database="IOT_PLATFORM"
    )

    dep_db_cursor = dep_db.cursor()

    sql = "SELECT App_run_type FROM Deployment_manager_db WHERE App_instance_ID = '{}'".format(app_instance_id)
    dep_db_cursor.execute(sql)
    result = dep_db_cursor.fetchone()

    if result is None:
        return False, None
    else:
        return True, result[0]

# app_instance_id = 'app_instance_63546eef86f64aec98c58e3ca96c38b3'

def get_app_id(app_instance_id):
    
    # def db_connection(filepath):
    filepath = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json(filepath)
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

    data = myresult[0]

    appid = data[0]
    return appid


def get_node_status(node_addr) :

    filepath = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    #get ip_add and port from node_addr
    ip_add = (node_addr.split())[0]
    port = (node_addr.split())[1]
    #execute the query : 
    query = "SELECT status FROM nodes WHERE ip='{}' AND port='{}'".format(ip_add,port)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    return myresult[0]


def get_node_username(node_addr) :
    filepath = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    #get ip_add and port from node_addrs
    ip_add = (node_addr.split())[0]
    port = (node_addr.split())[1]
    #execute the query : 
    query = "SELECT user FROM nodes WHERE ip='{ip}' AND port='{port}'".format(ip=ip_add,port=port)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    return myresult[0]
