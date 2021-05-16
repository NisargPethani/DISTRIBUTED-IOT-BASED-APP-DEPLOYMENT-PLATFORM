import mysql.connector
import json


def initialize():
  f = open ('configuration/scheduler_db.json', "r")
  data = json.loads(f.read())
  host_name = data["host"]
  user_name = data["user"]
  password = data["password"]
  database_name = data["database"]


  scheduler_DB = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password, auth_plugin='mysql_native_password'
  )

  mycursor = scheduler_DB.cursor()
  mycursor.execute("DROP DATABASE IF EXISTS scheduler")
  mycursor.execute("CREATE DATABASE IF NOT EXISTS scheduler")
  scheduler_DB.commit()
  mycursor.close()
  scheduler_DB.close()

  scheduler_DB = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,auth_plugin='mysql_native_password',
    database=database_name
  )

  mycursor = scheduler_DB.cursor()

  mycursor.execute("CREATE TABLE start_heap_table (appid VARCHAR(255) PRIMARY KEY, sdate VARCHAR(255),\
  stime VARCHAR(255), duration VARCHAR(255), repeatition VARCHAR(255), \
  interval_ VARCHAR(255), edate VARCHAR(255), etime VARCHAR(255))")

  mycursor.execute("CREATE TABLE job_queue_table (appid VARCHAR(255) PRIMARY KEY)")

  scheduler_DB.commit()
  mycursor.close()
  scheduler_DB.close()

initialize()