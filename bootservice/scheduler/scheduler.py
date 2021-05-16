from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import loads
import json
from createHeap import *
from scheduler_items import *
import threading
import datetime
from time import sleep
import mysql.connector
import heart_beat_client
from requests import get

print()
print()
print()
print()
print("*******************************************************************")
print(get('https://api.ipify.org').text)
print("*******************************************************************")
print()
print()
print()
print()
print()


def getKafka_credentials():
    f = open ('configuration/kafka_config.json', "r")
    data = json.loads(f.read())
    ip = data['ip']
    port = str(data['port'])
    return ip,port

def send_to_deployment_mgr(type1, message):
    ip, port = getKafka_credentials()
    producer = KafkaProducer(bootstrap_servers=[ip+':'+port], api_version=(0, 10, 1))
    message = type1 + ' standalone ' + message

    print("#####################################################################################")
    print(message)
    print("#####################################################################################")

    producer.send('run_application_topic', json.dumps(message).encode('utf-8'))
    producer.flush()
    producer.close()
    print('msg to dm sent to run')


def fun(app_instance_id):

    f = open ('configuration/db_config.json', "r")
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

    sql = "SELECT appid, sdate, stime, duration, repeatation, intervaltime FROM deploy where appinstanceid='"+app_instance_id+"'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    data = myresult[0]

    appid = data[0]
    sdate = data[1]
    stime = data[2]
    duration = data[3]
    repeatation = data[4]
    repeatation_bool = False

    if repeatation == "Yes":
        repeatation_bool = True
    else:
        repeatation_bool = False

    intervaltime = data[5]

    return sdate, stime, duration, repeatation_bool, intervaltime
    
    # return '2021-04-25','20:33','1', True, '2'

def get_cur_Time():
    cur_datetime = datetime.datetime.now()
    IST_date_time = cur_datetime + datetime.timedelta(minutes = 330)
    IST_date_time = str(IST_date_time)
    date, time = IST_date_time.split(' ')
    cur_time = (time.split('.'))[0]
    hour, minute, second = cur_time.split(':')
    return date, hour, minute

def get_start_date_time(start_date, start_time):
    date_time_str = start_date + ' ' + start_time
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    return date_time_obj

def get_date_time(start_date, start_time, duration, sec=False):
    start_date_time = get_start_date_time(start_date, start_time)
    if(sec==True):
        end_date_time = start_date_time + datetime.timedelta(seconds = duration)
    else:
        end_date_time = start_date_time + datetime.timedelta(minutes = duration)
    end_date, end_time = str(end_date_time).split(' ')
    h, m, s = end_time.split(':')
    end_time = h+':'+m
    return end_date, end_time
# (string,string,string,string,string,string,int,string) 
def insert_into_heap_table(app, start_date, start_time, end_date, end_time, duration, repetition, interval):
    f = open ('configuration/scheduler_db.json', "r")
    data = json.loads(f.read())
    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]

    scheduler_DB = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,auth_plugin='mysql_native_password',
    database=database_name
    )
    mycursor = scheduler_DB.cursor()

    sql = "INSERT INTO start_heap_table VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (app, start_date, start_time, duration, repetition, interval, end_date, end_time)
    mycursor.execute(sql, val)
    scheduler_DB.commit()
    scheduler_DB.close()

def update_start_heap_table(app,start_date, start_time, end_date, end_time):
    f = open ('configuration/scheduler_db.json', "r")
    data = json.loads(f.read())
    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]

    scheduler_DB = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,auth_plugin='mysql_native_password',
    database=database_name
    )
    mycursor = scheduler_DB.cursor()

    sql = "UPDATE start_heap_table SET sdate=%s,stime=%s,edate=%s,etime=%s WHERE appid=%s"
    val = (start_date, start_time, end_date, end_time, app)
    mycursor.execute(sql, val)
    scheduler_DB.commit()
    scheduler_DB.close()

def delete_from_start_heap_table(app):
    f = open ('configuration/scheduler_db.json', "r")
    data = json.loads(f.read())
    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]

    scheduler_DB = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,auth_plugin='mysql_native_password',
    database=database_name
    )
    mycursor = scheduler_DB.cursor()

    sql = "DELETE FROM start_heap_table WHERE appid = %s"
    val = (app,)
    mycursor.execute(sql, val)
    scheduler_DB.commit()
    scheduler_DB.close()

def insert_into_job_table(app):
    f = open ('configuration/scheduler_db.json', "r")
    data = json.loads(f.read())
    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]

    scheduler_DB = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,auth_plugin='mysql_native_password',
    database=database_name
    )
    mycursor = scheduler_DB.cursor()

    #check if app already in DB
    sql = "Select * from job_queue_table where appid = %s"
    val = (app,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    if(not data):
        sql = "INSERT INTO job_queue_table VALUES (%s)"
        val = (app,)
        mycursor.execute(sql, val)
    scheduler_DB.commit()
    scheduler_DB.close()

def delete_from_job_table(app):
    f = open ('configuration/scheduler_db.json', "r")
    data = json.loads(f.read())
    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]

    scheduler_DB = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,auth_plugin='mysql_native_password',
    database=database_name
    )
    mycursor = scheduler_DB.cursor()

    sql = "Select * from job_queue_table where appid = %s"
    val = (app,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    if(data):
        sql = "DELETE FROM job_queue_table WHERE appid = %s"
        val = (app,)
        mycursor.execute(sql, val)
        scheduler_DB.commit()
        scheduler_DB.close()

def stop_app(app):
    if(app in job_queue):
        job_queue.remove(app)
        delete_from_job_table(app)
        send_to_deployment_mgr('kill', app)
    else:
        print('app:',app,'is not running now')

# Listen to request from app_manager
class scheduler_input_(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
  
    def run(self):
        while True:
            print('listening')
            ip, port = getKafka_credentials()
            # print('#####ip:',ip,'port:',port,'##########')
            consumer = KafkaConsumer('appmanager_schedular',bootstrap_servers=[ip+':'+port],api_version=(0, 10))

            for message in consumer:
                print('msg:',message.value)
                msg = message.value.decode()
                break
            
            type1, app = msg.split(':')
            if('"' in type1):
                    type1 = type1.replace('"',"")
            if('"' in app):
                    app = app.replace('"',"")
            
            if(type1=='stop'):
                stop_app(app)
                continue
            
            start_date, start_time, duration, repetition, interval = fun(app)
            
            duration = int(duration)
            end_date, end_time = get_date_time(start_date, start_time, duration)
            
            if(repetition==False):
                interval = 0
            else:
                interval = int(interval)
                interval = interval - duration

            if(repetition==True):
                repeat = "True"
            else:
                repeat = "False"
            insert_into_heap_table(app, start_date, start_time, end_date, end_time, str(duration),repeat,str(interval))

            if(type1=='start'):
                print("starting app")
                start_app(start_date, start_time, end_date, end_time, app, duration, interval)
                # print('came out')

# monitor start time heaps
class monitor_start_heap(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
        
    def run(self): 
        
        while(True):
            today, HH, MM = get_cur_Time()
            hour = get_time(HH)
            minute = get_time(MM)
            
            if(len(start_heap)>0):
                # this_date_time = get_start_date_time(today, str(hour)+':'+str(minute))
                # to_start_date_time = get_start_date_time(start_heap[0].date_, str(start_heap[0].hour)+':'+str(start_heap[0].minute))
                # if(this_date_time > to_start_date_time):

                if(len(start_heap)>0 and start_heap[0].date_==today and start_heap[0].hour==hour and (start_heap[0].minute==minute or start_heap[0].minute==minute-1)):         
                    app = start_heap[0].uuid
                    heapq.heappop(start_heap)
                    if(app not in job_queue):
                        insert_into_job_table(app)
                        job_queue.append(app)
                        #now send this app value to deployment manager
                        print('sending to dm to run app')
                        send_to_deployment_mgr('start', app)
                    
# monitor end time heap
class monitor_end_heap(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
        
    def run(self): 
        # hour, minute = get_cur_Time()
        
        while(True):
            
            today, HH, MM = get_cur_Time()
            hour = get_time(HH)
            minute = get_time(MM)
            
            if(len(end_heap)>0 and end_heap[0].date_==today and end_heap[0].hour==hour and end_heap[0].minute==minute):
                app = end_heap[0].uuid

                if(app in job_queue):
                    job_queue.remove(app)
                    delete_from_job_table(app)
                    #now send this app value to deployment manager
                    print('sending kill to dm')
                    send_to_deployment_mgr('kill', app)

                if(end_heap[0].interval > 0):
                    start_date, start_time = get_date_time(today, str(HH+':'+MM), end_heap[0].interval)
                    end_date, end_time = get_date_time(start_date, start_time, end_heap[0].duration)
                    print('restarting:', start_date, start_time, end_date, end_time)
                    start_app(start_date, start_time, end_date, end_time, app, end_heap[0].duration, end_heap[0].interval)
                    update_start_heap_table(app,start_date, start_time, end_date, end_time)
                else:
                    delete_from_start_heap_table(app)
                heapq.heappop(end_heap)
                

def restore_state():
    f = open ('configuration/scheduler_db.json', "r")
    data = json.loads(f.read())
    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]

    scheduler_DB = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,auth_plugin='mysql_native_password',
    database=database_name
    )
    mycursor = scheduler_DB.cursor()

    print('########### RESTORING PREVIOUS STATE #############')
    mycursor.execute("SELECT * FROM job_queue_table")
    myresult = mycursor.fetchall()
    for x in myresult:
        app = x[0]
        job_queue.append(app)
    
    mycursor.execute("SELECT * FROM start_heap_table")
    myresult = mycursor.fetchall()
    gap = 5
    for x in myresult:
        # print(x)
        app, sdate, stime, duration, repeatation, interval, edate, etime = x
        print('restoring app:',app)
        duration = int(duration)
        interval = int(interval)
        start_date_time = get_start_date_time(sdate, stime)
        end_date_time = get_start_date_time(edate, etime)
        date, H, M = get_cur_Time()
        cur_date_time = get_start_date_time(date, H+':'+M)

        if(cur_date_time <= end_date_time and cur_date_time >= start_date_time):
            start_app(sdate, stime, edate, etime, app, duration, interval)
        
        elif(start_date_time >= cur_date_time):
            start_app(sdate, stime, edate, etime, app, duration, interval)
        else:
            cnt=0

            while(True):


                date, H, M = get_cur_Time()
                cur_date_time = get_start_date_time(date, H+':'+M)

                new_start_date, new_start_time = get_date_time(sdate, stime, (duration+interval)*cnt)
                new_start_date_time = get_start_date_time(new_start_date, new_start_time)

                new_end_date, new_end_time = get_date_time(new_start_date, new_start_time, duration)
                new_end_date_time = get_start_date_time(new_end_date, new_end_time)

                if((cur_date_time <= new_start_date_time and cur_date_time <= new_end_date_time) or (new_start_date_time <= cur_date_time and cur_date_time <= new_end_date_time)):
                    break
                cnt += 1

            # print('new Dates:', new_start_date, new_start_time, new_end_date, new_end_time)
            start_app(new_start_date, new_start_time, new_end_date, new_end_time, app, duration, interval)
    
    mycursor.close()


#init methods
heart_beat_client.start_heart_beat()
restore_state()
get_input_thread = scheduler_input_()
start_time_thread = monitor_start_heap() 
end_time_thread = monitor_end_heap()

get_input_thread.start()
start_time_thread.start()
end_time_thread.start() 
