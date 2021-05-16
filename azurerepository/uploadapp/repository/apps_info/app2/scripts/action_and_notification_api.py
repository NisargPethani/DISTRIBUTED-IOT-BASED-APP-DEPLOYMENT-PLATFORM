import socket
import threading
import sys
import mysql.connector

serverIp = '127.0.0.1'
port = 8081

def getappnameandusername(appinstanceid):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hackathon"
    )

    mycursor = mydb.cursor()

    sql = "SELECT username, appid FROM deploy where appinstanceid='"+appinstanceid+"'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    
    username = myresult[0][0]
    appid = myresult[0][1]

    sql = "SELECT name FROM apps where id='"+appid+"'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    
    appname = myresult[0][0]

    return username, appname

def send_notification(notif_message):
    try:
        sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
    except socket.error as error:
        print("Socket creation failed with error :", error)
        sys.exit(0)
    try:
        app_id = sys.argv[1]

        username, appname = getappnameandusername(app_id)

        userstr = [appname, username]
        userstr = str(userstr)

        notif_message = userstr + ":" + " " + notif_message
        sockt.connect((serverIp, port))
        sockt.send(notif_message.encode())
        data = sockt.recv(1024).decode()
        if data=="1":
            print("notification recieved successefully..")

    except socket.error as error:
        print("Socket connection failed with error :", error)
        sys.exit(0)

            
    

