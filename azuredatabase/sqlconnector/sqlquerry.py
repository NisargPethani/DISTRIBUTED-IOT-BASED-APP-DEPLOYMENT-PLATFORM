import mysql.connector
import ast
import json

import os
os.system('clear')

def read_json(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]
    return host_name, user_name, password, database_name


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
tables = []

print("#################################################")
print("#################################################")
print("#################################################")
print("Pethani- Tables")

print("#################################################")
print("Tables")

sql= "SHOW TABLES"
mycursor.execute(sql)

myresult = mycursor.fetchall()
for i in myresult:
    tables.append(i[0])

print()

adityatables = {"nodes"}

for t in tables:
    
    if t in adityatables:
        continue

    print("#################################################")
    print(t)

    sql= "SELECT * FROM "+t
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    for i in myresult:
        print(i)

    print()

print()
print()
print()
print()
print()
print("#################################################")
print("#################################################")
print("#################################################")
print("Aditya- Tables")

print("#################################################")
print("nodes")

sql= "SELECT * FROM nodes"
mycursor.execute(sql)

myresult = mycursor.fetchall()
for i in myresult:
    print(i)

print()

##############################################################################

# def db_connection(filepath):
filepath = "configuration/db_config.json"
host_name, user_name, password, database_name = read_json(filepath)
dep_db = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,
    database="IOT_PLATFORM"
)
dep_db_cursor = dep_db.cursor()
tables = []

print()
print()
print()
print()
print()
print("#################################################")
print("#################################################")
print("#################################################")
print("Akshat- Tables")

sql= "SHOW TABLES"
dep_db_cursor.execute(sql)

myresult = dep_db_cursor.fetchall()
for i in myresult:
    tables.append(i[0])

print()

for t in tables:
    print("#################################################")
    print(t)

    sql= "SELECT * FROM "+t
    dep_db_cursor.execute(sql)

    myresult = dep_db_cursor.fetchall()
    for i in myresult:
        print(i)

    print()
    
    
    
######################################################
# Chitra

f = open ('configuration/scheduler_db.json', "r")

data = json.loads(f.read())

host_name = data["host"]
user_name = data["user"]
password = data["password"]
database_name = data["database"]

scheduler_DB = mysql.connector.connect(
	host=host_name,
	user=user_name,
	password=password,
	database=database_name
)

mycursor = scheduler_DB.cursor()


print()
print()
print()
print()
tables = []
print("#################################################")
print("#################################################")
print("#################################################")
print("Chitra- Tables")

sql= "SHOW TABLES"
mycursor.execute(sql)

myresult = mycursor.fetchall()
for i in myresult:
    tables.append(i[0])

print()

for t in tables:
    print("#################################################")
    print(t)

    sql= "SELECT * FROM "+t
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    for i in myresult:
        print(i)

    print()

