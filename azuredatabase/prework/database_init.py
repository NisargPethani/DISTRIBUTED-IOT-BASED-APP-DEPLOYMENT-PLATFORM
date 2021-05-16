import mysql.connector
import json


# JSON file
f = open ('configuration/db_config.json', "r")
  
# Reading from file
data = json.loads(f.read())


host_name = data["host"]
user_name = data["user"]
password = data["password"]
database_name = data["database"]

# print(host_name, user_name, password, database_name)

mydb = mysql.connector.connect(
  host=host_name,
  user=user_name,
  password=password
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS {}".format(database_name))
mycursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))

mydb = mysql.connector.connect(
  host=host_name,
  user=user_name,
  password=password,
  database=database_name
)


mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255))")

mycursor.execute("CREATE TABLE sensorinstance (id VARCHAR(255) PRIMARY KEY, sensor_type_id VARCHAR(255), ip VARCHAR(255), port int, loc_room int, loc_house int, loc_street VARCHAR(255), loc_city VARCHAR(255))")
mycursor.execute("CREATE TABLE sensorinstanceipport (ip VARCHAR(255) NOT NULL, port int NOT NULL, id VARCHAR(255), PRIMARY KEY (ip, port))")

mycursor.execute("CREATE TABLE controllerinstance (id VARCHAR(255) PRIMARY KEY, controller_type_id VARCHAR(255), ip VARCHAR(255), port int, loc_room int, loc_house int, loc_street VARCHAR(255), loc_city VARCHAR(255))")
mycursor.execute("CREATE TABLE controllerinstanceipport (ip VARCHAR(255) NOT NULL, port int NOT NULL, id VARCHAR(255), PRIMARY KEY (ip, port))")

mycursor.execute("CREATE TABLE sensortypes (sensor_type_id VARCHAR(255) PRIMARY KEY, sensor_type VARCHAR(255), fieldcount int, fields VARCHAR(1023), datarate VARCHAR(255), company VARCHAR(255), model VARCHAR(255))")
mycursor.execute("CREATE TABLE controllertypes (controller_type_id VARCHAR(255) PRIMARY KEY, controller_type VARCHAR(255), input VARCHAR(255), company VARCHAR(255), model VARCHAR(255))")

mycursor.execute("CREATE TABLE apps (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), sensorcount int, sensortype VARCHAR(1023), controllercount int, controllertype VARCHAR(1023))")

mycursor.execute("CREATE TABLE deploy (appinstanceid VARCHAR(255) PRIMARY KEY, username VARCHAR(255), appid VARCHAR(255), sdate VARCHAR(255), stime VARCHAR(255), duration int, repeatation VARCHAR(5), intervaltime int, algonum int)")


######new tables
mycursor.execute("CREATE TABLE developers (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255))")
mycursor.execute("CREATE TABLE configurers (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255))")
