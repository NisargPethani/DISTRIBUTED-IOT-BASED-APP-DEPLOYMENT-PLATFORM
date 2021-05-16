import mysql.connector
import json
import sys

# JSON file
f = open ('configuration/db_config.json', "r")
  
# Reading from file
data = json.loads(f.read())


host_name = data["host"]
user_name = data["user"]
password = data["password"]
database_name = data["database"]

mydb = mysql.connector.connect(
  host=host_name,
  user=user_name,
  password=password,
  database=database_name
)

mycursor = mydb.cursor()

table_name = sys.argv[1]
if table_name == "":
  raise NotImplementedError

mycursor.execute("DELETE FROM {}".format(table_name))
mydb.commit()