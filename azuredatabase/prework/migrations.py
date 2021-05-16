import mysql.connector
import sys
import json
  
f = open('./configuration/db_config.json','r')
db_config = json.load(f)
f.close()

dep_db = mysql.connector.connect(
  host=db_config["host"],
  user=db_config["user"],
  password=db_config["password"]
)

dep_db_cursor = dep_db.cursor()

dep_db_cursor.execute("DROP DATABASE IF EXISTS IOT_PLATFORM")
dep_db_cursor.execute("CREATE DATABASE IOT_PLATFORM")
dep_db_cursor.execute("USE IOT_PLATFORM")
dep_db_cursor.execute("CREATE TABLE Deployment_manager_db (Job_ID VARCHAR(32), App_instance_ID VARCHAR(45), Server_address VARCHAR(36), App_run_type VARCHAR(36))")

dep_db_cursor.close()
dep_db.close()

