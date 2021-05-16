def read_json(filepath):
 f = open (filepath, "r")
 
 # Reading from file
 data = json.loads(f.read())
 
 host_name = data["host"]
 user_name = data["user"]
 password = data["password"]
 database_name = data["database"]
 return host_name, user_name, password, database_name
 
def getappnameandusername(appinstanceid):
    # def db_connection(filepath):
    filepathdb = "db_config.json"
    host_name, user_name, password, database_name = read_json(filepathdb)
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database=database_name
    )
    mycursor = mydb.cursor()

    sql = "SELECT username, appid FROM deploy where appinstanceid='"+appinstanceid+"'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    username = myresult[0][0]
    appid = myresult[0][1]
    return  appid