import mysql.connector
import json

# JSON file
f = open ('./configuration/db_config.json', "r")
# Reading from file
data = json.loads(f.read())
host_name = data["host"]
user_name = data["user"]
password = data["password"]
database_name = data["database"]

# def read_json(filepath):
#     f = open (filepath, "r")
  
#     # Reading from file
#     data = json.loads(f.read())

#     host_name = data["host"]
#     user_name = data["user"]
#     password = data["password"]
#     database_name = data["database"]
#     return host_name, user_name, password, database_name

print(host_name, user_name, password, database_name)

mydb = mysql.connector.connect(
  host=host_name,
  user=user_name,
  password=password
)

mycursor = mydb.cursor()
# mycursor.execute("DROP DATABASE IF EXISTS hackathon")
mycursor.execute("CREATE DATABASE IF NOT EXISTS hackathon")

mydb = mysql.connector.connect(
  host=host_name,
  user=user_name,
  password=password,
  database=database_name
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE nodes (ip VARCHAR(255) NOT NULL, port VARCHAR(255) NOT NULL, status VARCHAR(255) NOT NULL, user VARCHAR(255) NOT NULL, PRIMARY KEY(ip,port))")


# mycursor.execute("INSERT INTO nodes VALUES('127.0.0.1', '8089', 'active');")
# mycursor.execute("INSERT INTO nodes VALUES('127.0.0.1', '8090', 'active');")
# mydb.commit()

# # fetch active nodes
# select ip, port from nodes where status='active'
# # fetch free nodes
# select ip, port from nodes where status='free'
# # fetch one free node
# select ip, port from nodes where status='free' limit 1
# # set active
# update nodes set status = 'active' where ip = ip and port = port
# # insert free node
# update nodes set status = 'free' where ip = ip and port = port




# def fetch_active_nodes(mydb, mycursor):
#     myresult = [] 
#     mycursor.execute("select ip, port from nodes where status='active'")
#     myresult = mycursor.fetchall()
    
#     for i in range(len(myresult)):
#         myresult[i][1] = int(myresult[i][1])
#     return myresult

# def fetch_one_free_nodes(mydb, mycursor):
#     myresult = [] 

#     mycursor.execute("select ip, port from nodes where status='free' limit 1")
#     myresult = mycursor.fetchall()
    
#     for i in range(len(myresult)):
#         myresult[i][1] = int(myresult[i][1])
#     return myresult

# def set_active(mydb, mycursor, ip, port):
#     port = str(port)
#     mycursor.execute("update nodes set status = 'active' where ip = {} and port = {}".format(ip,port))
#     mydb.commit()

# def insert_free_node(mydb, mycursor, ip, port):
#     port = str(port)
#     mycursor.execute("insert into nodes values({}, {}, {}) ".format(ip,port, 'free'))
#     mydb.commit()

# def insert_active_node(mydb, mycursor, ip, port):
#     port = str(port)
#     mycursor.execute("insert into nodes values({}, {}, {}) ".format(ip,port, 'active'))
#     mydb.commit()



# # myresult = fetch_active_nodes(mydb,mycursor)
# # print(myresult, type(myresult))


# # myresult =fetch_one_free_nodes(mydb, mycursor):
# # print(myresult, type(myresult))


# myresult = fetch_one_free_nodes(mydb, mycursor)
# print("My_result :", myresult)




