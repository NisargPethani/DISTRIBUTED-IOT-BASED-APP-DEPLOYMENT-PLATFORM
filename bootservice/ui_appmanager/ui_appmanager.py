from flask import Flask, render_template, redirect, url_for, request, session
import mysql.connector
import uuid
import sensor_instance_validator
import sensor_type_validator
import app_validator
import deploy_validator
import controller_type_validator
import controller_instance_validator
from kafka import KafkaConsumer
import shutil
import os
import json
from kafka.structs import TopicPartition
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

heart_beat_client.start_heart_beat()

def read_json_db(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    host_name = data["host"]
    user_name = data["user"]
    password = data["password"]
    database_name = data["database"]
    return host_name, user_name, password, database_name



def read_json_kafka(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    ip = data["ip"]
    port = data["port"]

    return ip, port

    # filepathkafka = "configuration/kafka_config.json"
    # kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    # '{}:{}'.format(kafka_ip,kafka_port)

app = Flask(__name__)
app.secret_key = "SECREATE_KEY"  

all_link_str = "<br><br><br><br><a href=\"/signup\"><button>Go to Signup Page</button></a> <br><br><a href=\"/login\"><button>Go to Login Page</button></a> &nbsp&nbsp<a href=\"/logout\"><button>Go to Logout Page</button></a><br><br><a href=\"/sensor_type_upload\"><button>Go to Sensor Type Upload Page</button></a> &nbsp&nbsp<a href=\"/sensor_instance_upload\"><button>Go to Sensor Instance Upload Page</button></a><br><br><a href=\"/controller_type_upload\"><button>Go to Controller Type Upload Page</button></a> &nbsp&nbsp<a href=\"/controller_instance_upload\"><button>Go to Controller Instance Upload Page</button></a><br><br><a href=\"/app_upload\"><button>Go to App Upload Page</button></a> &nbsp&nbsp<a href=\"/deploy_upload\"><button>Go to App Deploy Page</button></a><br><br>"

#####################################################################################       Signup 

def insertdata(tablename, data_hdr, data):
    
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    hdr_str = ", ".join(i for i in data_hdr)
    sql = "INSERT INTO "+tablename+" ("+hdr_str+") VALUES ("+str(data)[1:-1]+")"

    mycursor.execute(sql)
    
    mydb.commit()

@app.route('/signupsucess/<username>')
def signupsucess(username):

    html_code = username + " Registered" + all_link_str
    return  html_code

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(username)
        print(password)

        try:
            insertdata('users', ['username', 'password'],[username, password])
        except Exception:
            error = "Username alredy taken/ Empty credntials"
            return render_template('signup.html', error=error)

        # kafka_topic.create_topic(username)

        return redirect(url_for('login', username=username))

    return render_template('signup.html', error=error)


#####################################################################################       Login

def isuserexist(tablename, data_hdr, data):
    
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    sql = "SELECT * FROM "+tablename+" WHERE "+data_hdr[0]+"='"+data[0]+"' and "+data_hdr[1]+"='"+data[1]+"'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        return True
    else:
        return False

@app.route('/loginsucess/<username>')
def loginsucess(username):

    html_code = "Logged in.... Welcome " + username + all_link_str
    return  html_code

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user_flag = isuserexist('users',['username', 'password'],[username, password])

            if user_flag == True:
                session['loggedin_user'] = True
                session['username_user'] = username

                #return redirect(url_for('deploy_upload', username=username))
                return redirect(url_for('homeuser', username=username))
            else:
                error = "Wrong credentials... Try Again!!!" 
                return render_template('login.html', error=error)

        except Exception:
            error = "Wrong credentials... Try Again!!!" 
            return render_template('login.html', error=error)

    return render_template('login.html', error=error)

################################################################################################## new changes
@app.route('/homeuser')
def homeuser():
     return render_template('indexuser.html')

#####################################################################################       logout

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    
    session.pop('loggedin_user', None)
    session.pop('username_user',None)

    session.pop('loggedin_dev', None)
    session.pop('username_dev',None)

    session.pop('loggedin_confi', None)
    session.pop('username_confi',None)    

    return redirect(url_for('home'))


#####################################################################################       notification

@app.route('/notification', methods=['GET', 'POST'])
def notification():

    try:
        login_flag = session['loggedin_user']
    except Exception:        
        error = "No Logged in User"
        return error

    username = session['username_user']
    heading = "Notification for username: " + username + "<br><br>"


    filepathkafka = "configuration/kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepathkafka)

    # '{}:{}'.format(kafka_ip,kafka_port)

    consumer = KafkaConsumer(bootstrap_servers = ['{}:{}'.format(kafka_ip,kafka_port)], api_version = (0,10),consumer_timeout_ms = 1000, auto_offset_reset="earliest")
    # consumer.seek_to_beginning()
    
    partition = TopicPartition(username, 0)
    
    consumer.assign([partition])
    consumer.seek(partition, 0)

    notification_string = ""    

    for message in consumer:
        notification_string += str(message.value) + "<br>" 

    # notification_string += "<br><br><br><br>" + str(message.offset) 

    return heading + notification_string + all_link_str

#####################################################################################       Upload-controller_instance

@app.route('/controller_instance_upload')
def controller_instance_upload():
    error = ""
    return render_template('controller_instance_upload.html', error=error)

@app.route('/controller_instance_uploader', methods=['POST'])
def controller_instance_uploader():

    try:
       login_flag = session['loggedin_confi']
    except Exception:        
       error = "No Logged in Application Configurer"
       return render_template('controller_instance_upload.html', error=error)

    uploaded_file = request.files['file']

    try: 
        shutil.rmtree("temp/")
    except Exception:
        pass
    
    os.mkdir("temp")

    if uploaded_file.filename != '':

        name = "temp/" + uploaded_file.filename
        uploaded_file.save(name)
        flag1,mess = controller_instance_validator.controller_instance_validator(name)
        if(flag1==True):
        	return render_template('controller_instance_upload.html', message=("Validation successful: " + mess))
        else:
        	return render_template('controller_instance_upload.html', error=("Validation Failed: " + mess))
    else:
        return render_template('controller_instance_upload.html',error="No file choosen")  

#####################################################################################       Upload-sensor_instance

@app.route('/sensor_instance_upload')
def sensor_instance_upload():
    error = ""
    return render_template('sensor_instance_upload.html', error=error)

@app.route('/sensor_instance_uploader', methods=['POST'])
def sensor_instance_uploader():

    try:
       login_flag = session['loggedin_confi']
    except Exception:        
       error = "No Logged in Application Configurer"
       return render_template('sensor_instance_upload.html', error=error)

    uploaded_file = request.files['file']

    try: 
        shutil.rmtree("temp/")
    except Exception:
        pass
    
    os.mkdir("temp")

    if uploaded_file.filename != '':

        name = "temp/" + uploaded_file.filename
        uploaded_file.save(name)
        flag1,mess = sensor_instance_validator.sensor_instance_validator(name)
        if(flag1==True):
        	return render_template('sensor_instance_upload.html', message=("Validation successful: " + mess))
        else:
        	return render_template('sensor_instance_upload.html', error=("Validation Failed: " + mess))
    else:
        return render_template('sensor_instance_upload.html',error="No file choosen")    

#####################################################################################       Upload-sensor_type

@app.route('/sensor_type_upload')
def sensor_type_upload():
    error = ""
    return render_template('sensor_type_upload.html', error=error)

@app.route('/sensor_type_uploader', methods=['POST'])
def sensor_type_uploader():
    
    try:
       login_flag = session['loggedin_confi']
    except Exception:        
       error = "No Logged in Application Configurer"
       return render_template('sensor_type_upload.html', error=error)

    uploaded_file = request.files['file']

    try: 
        shutil.rmtree("temp/")
    except Exception:
        pass
    
    os.mkdir("temp")

    if uploaded_file.filename != '':

        name = "temp/" + uploaded_file.filename
        uploaded_file.save(name)
        flag1,mess = sensor_type_validator.sensor_type_validator(name)
        if(flag1==True):
        	return render_template('sensor_type_upload.html', message=("Validation successful: " + mess))
        else:
        	return render_template('sensor_type_upload.html', error=("Validation Failed: " + mess))
    else:
        return render_template('sensor_type_upload.html',error="No file choosen")    

#####################################################################################       Upload-controller_type

@app.route('/controller_type_upload')
def controller_type_upload():
    error = ""
    return render_template('controller_type_upload.html', error=error)

@app.route('/controller_type_uploader', methods=['POST'])
def controller_type_uploader():
    
    try:
       login_flag = session['loggedin_confi']
    except Exception:        
       error = "No Logged in Application Configurer"
       return render_template('controller_type_upload.html', error=error)

    uploaded_file = request.files['file']

    try: 
        shutil.rmtree("temp/")
    except Exception:
        pass
    
    os.mkdir("temp")

    if uploaded_file.filename != '':

        name = "temp/" + uploaded_file.filename
        uploaded_file.save(name)
        flag1,mess = controller_type_validator.controller_type_validator(name)
        if(flag1==True):
        	return render_template('controller_type_upload.html', message=("Validation successful: " + mess))
        else:
        	return render_template('controller_type_upload.html', error=("Validation Failed: " + mess))   
    else:
        return render_template('controller_type_upload.html',error="No file choosen")       


#####################################################################################       Upload-app

@app.route('/app_upload')
def app_upload():
    error = ""
    return render_template('app_upload.html', error=error)

@app.route('/app_uploader', methods=['POST'])
def app_uploader():
    
    try:
       login_flag = session['loggedin_dev']
    except Exception:        
       error = "No Logged in  Application Developer"
       return render_template('app_upload.html', error=error)

    uploaded_file = request.files['file']

    try: 
        shutil.rmtree("temp/")
    except Exception:
        pass
    
    os.mkdir("temp")

    if uploaded_file.filename != '':

        name = "temp/" + uploaded_file.filename
        uploaded_file.save(name)
        flag1,mess = app_validator.app_validator(name)
        if(flag1==True):
        	return render_template('app_upload.html', message=("Validation successful: "+mess))
        else:
        	return render_template('app_upload.html', error=("Validation Failed: "+mess)) 
    else:
        return render_template('app_upload.html',error="No file choosen") 

#####################################################################################       Upload-sensor_type

def getappinfostr():
    filepathdb = "configuration/db_config.json"
    host_name, user_name, password, database_name = read_json_db(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    sql= "SELECT id, name FROM apps"
    mycursor.execute(sql)

    return_str = "\n\n"

    myresult = mycursor.fetchall()
    for i in myresult:
        return_str = return_str + str(i) + " \n"

    return return_str

@app.route('/deploy_upload')
def deploy_upload():
    error = ""
    appinfo = getappinfostr()
    return render_template('deploy_upload.html', error=error, appinfo=appinfo)

@app.route('/deploy_uploader', methods=['POST'])
def deploy_uploader():
    
    try:
        login_flag = session['loggedin_user']
    except Exception:        
        error = "No Logged in User"
        appinfo = getappinfostr()
        return render_template('deploy_upload.html', error=error, appinfo=appinfo)

    username = session['username_user']
        
    appid = request.form['appid']
    stime = request.form['stime']
    duration = request.form['duration']
    locroom = request.form['locroom']
    lochouse = request.form['lochouse']
    locstreet = request.form['locstreet']
    loccity= request.form['loccity']

    algonum = request.form['algonum']
    
    locflag = request.form['loc']

    if locflag == "No":
        locroom="0"
        lochouse="0"
        locstreet="UNK"

    sdate = request.form['sdate']
    repeatation = request.form['repeatation']

    if repeatation == "Yes":

        ryear = int(request.form['ryear'])
        rmonth = int(request.form['rmonth'])
        rday = int(request.form['rday'])
        rhour = int(request.form['rhour'])
        rmin = int(request.form['rmin'])
        
        interval_time = ryear * 525600 + rmonth * 43800 + rday * 1440 + rhour * 60 + rmin 
        if interval_time == 0:
            error = "Invalid Interval Time"
            appinfo = getappinfostr()
            return render_template('deploy_upload.html', error=error, appinfo=appinfo)
    else:
        interval_time= -1

    deploy_data=[username, appid, stime, duration, locroom, lochouse, locstreet, loccity, repeatation, interval_time, sdate, algonum]

    mess = deploy_validator.deploy_validator(deploy_data)
    if(mess == "App Deploment started"):
        return render_template('deploy_upload.html', message=mess)
    else:
        return render_template('deploy_upload.html', error=mess)
    #deploy_validator.deploy_validator(deploy_data) + all_link_str

################################################################################################## new changes
@app.route('/signupdev', methods=['GET', 'POST'])
def signupdev():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(username)
        print(password)

        try:
            insertdata('developers', ['username', 'password'],[username, password])
        except Exception:
            error = "Username alredy taken/ Empty credntials"
            return render_template('signupdev.html', error=error)

        return redirect(url_for('logindev', username=username))

    return render_template('signupdev.html', error=error)

################################################################################################## new changes
@app.route('/logindev', methods=['GET', 'POST'])
def logindev():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user_flag = isuserexist('developers',['username', 'password'],[username, password])

            if user_flag == True:

                session['loggedin_dev'] = True
                session['username_dev'] = username

                return redirect(url_for('app_upload', username=username))
            else:
                error = "Wrong credentials... Try Again!!!" 
                return render_template('logindev.html', error=error)

        except Exception:
            error = "Wrong credentials... Try Again!!!" 
            return render_template('logindev.html', error=error)

    return render_template('logindev.html', error=error)
    
################################################################################################## new changes
@app.route('/signupconfi', methods=['GET', 'POST'])
def signupconfi():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        key = request.form['key']
        if(key=="group7@123"):

            print(username)
            print(password)

            try:
                insertdata('configurers', ['username', 'password'],[username, password])
            except Exception:
                error = "Username alredy taken/ Empty credntials"
                return render_template('signupconfi.html', error=error)

            return redirect(url_for('loginconfi', username=username))
        else:
            error = "Wrong Key inserted"
            return render_template('signupconfi.html', error=error)

    return render_template('signupconfi.html', error=error)

################################################################################################## new changes
@app.route('/loginconfi', methods=['GET', 'POST'])
def loginconfi():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user_flag = isuserexist('configurers',['username', 'password'],[username, password])

            if user_flag == True:

                session['loggedin_confi'] = True
                session['username_confi'] = username

                return redirect(url_for('homeconfi'))
            else:
                error = "Wrong credentials... Try Again!!!" 
                return render_template('loginconfi.html', error=error)

        except Exception:
            error = "Wrong credentials... Try Again!!!" 
            return render_template('loginconfi.html', error=error)

    return render_template('loginconfi.html', error=error)
    
################################################################################################## new changes
@app.route('/homeconfi')
def homeconfi():
     return render_template('indexconfi.html')
     
#####################################################################################       Start

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=5002)

    session.pop('loggedin_user', None)
    session.pop('username_user',None)

    session.pop('loggedin_dev', None)
    session.pop('username_dev',None)

    session.pop('loggedin_confi', None)
    session.pop('username_confi',None)
