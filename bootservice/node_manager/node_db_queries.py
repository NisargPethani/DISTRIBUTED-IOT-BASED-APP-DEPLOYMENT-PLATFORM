import mysql.connector
import json

filepath = "./configuration/db_config.json"

def read_json(filepath):
    f = open (filepath, "r")
    # Reading from file
    data = json.loads(f.read())

    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]
    return host_name, user_name, password, database_name

def connectfun():
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

def fetch_active_nodes():
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    myresult = [] 
    mycursor.execute("select ip, port, user from nodes where status='active'")
    myresult = mycursor.fetchall()
    
    active_nodes = []
    for node in myresult:
        active_nodes.append((node[0], int(node[1]), node[2]))
    return active_nodes

def fetch_free_node():
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    free_node = [] 
    mycursor.execute("select ip, port, user from nodes where status='free' limit 1;")
    myresult = mycursor.fetchall()
    
    free_node = []
    for node in myresult:
        free_node.append((node[0], int(node[1]), node[2]))
    return free_node

def set_active(ip, port,user):
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    port = str(port)
    mycursor.execute("update nodes set status = 'active' where ip = '{}' and port = '{}' and user = '{}';".format(ip,port,user))
    mydb.commit()

def set_deleted(ip, port):
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    port = str(port)
    mycursor.execute("update nodes set status = 'deleted' where ip = '{}' and port = '{}';".format(ip,port))
    mydb.commit()


def insert_free_node(ip, port, user):
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    port = str(port)
    
    mycursor.execute("select * from nodes where ip = '{}' and port = '{}' and user = '{}';".format(ip,port,user))
    myresult = mycursor.fetchall()
    if len(myresult) >0:
        mycursor.execute("update nodes set status = 'active' where ip = '{}' and port = '{}' and user = '{}';".format(ip,port,user))
    else:
        mycursor.execute("insert into nodes values('{}', '{}', '{}', '{}');".format(ip,port, "free", user))  ## deleted
    mydb.commit()

def insert_active_node(ip, port, user):
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    print("ip :", ip ," port:", port)
    port = str(port)
    mycursor.execute("select * from nodes where ip = '{}' and port = '{}' and user = '{}';".format(ip,port,user))
    myresult = mycursor.fetchall()
    if len(myresult) >0:
        mycursor.execute("update nodes set status = 'active' where ip = '{}' and port = '{}' and user = '{}';".format(ip,port,user))
    else:
        mycursor.execute("insert into nodes values('{}', '{}', '{}', '{}');".format(ip,port, "active", user))
    mydb.commit()

def delete_node(ip, port, user):
    host_name, user_name, password, database_name = read_json(filepath)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()
    port = str(port)
    mycursor.execute("Delete from nodes where ip = '{}'and port = '{}' and user = '{}';".format(ip,port, user))
    mydb.commit()

