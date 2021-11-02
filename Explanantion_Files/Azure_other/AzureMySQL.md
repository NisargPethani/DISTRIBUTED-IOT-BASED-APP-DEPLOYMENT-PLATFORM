# Azure MySQL

```python
import mysql.connector

mydb = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password,
    database=database_name
)

mycursor = mydb.cursor()
mycursor.execute("QUERY"))
```
---

## DataBases

### Users, Application Developers & Application Configures

```sql
CREATE TABLE users (
    username VARCHAR(255) PRIMARY KEY, 
    password VARCHAR(255)
)

CREATE TABLE developers (
    username VARCHAR(255) PRIMARY KEY, 
    password VARCHAR(255)
)

CREATE TABLE configurers (
    username VARCHAR(255) PRIMARY KEY, 
    password VARCHAR(255)
)
```

### Sensor & Controller

```sql
CREATE TABLE sensorinstance (
    id VARCHAR(255) PRIMARY KEY,
    sensor_type_id VARCHAR(255),
    ip VARCHAR(255),
    port int,
    loc_room int,
    loc_house int,
    loc_street VARCHAR(255),
    loc_city VARCHAR(255)
)

CREATE TABLE sensorinstanceipport (
    ip VARCHAR(255) NOT NULL,
    port int NOT NULL,
    id VARCHAR(255),
    PRIMARY KEY (ip,
    port)
)

CREATE TABLE controllerinstance (
    id VARCHAR(255) PRIMARY KEY,
    controller_type_id VARCHAR(255),
    ip VARCHAR(255),
    port int,
    loc_room int,
    loc_house int,
    loc_street VARCHAR(255),
    loc_city VARCHAR(255)
)

CREATE TABLE controllerinstanceipport (
    ip VARCHAR(255) NOT NULL,
    port int NOT NULL,
    id VARCHAR(255),
    PRIMARY KEY (ip,
    port)
)

CREATE TABLE sensortypes (
    sensor_type_id VARCHAR(255) PRIMARY KEY,
    sensor_type VARCHAR(255),
    fieldcount int,
    fields VARCHAR(1023),
    datarate VARCHAR(255),
    company VARCHAR(255),
    model VARCHAR(255)
)

CREATE TABLE controllertypes (
    controller_type_id VARCHAR(255) PRIMARY KEY,
    controller_type VARCHAR(255),
    input VARCHAR(255),
    company VARCHAR(255),
    model VARCHAR(255)
)
```

### Application

```sql
CREATE TABLE apps (
    id VARCHAR(255) PRIMARY KEY, 
    name VARCHAR(255), 
    sensorcount int, 
    sensortype VARCHAR(1023), 
    controllercount int, 
    controllertype VARCHAR(1023)
)
```

### Schedular

```sql
CREATE TABLE start_heap_table (
    appid VARCHAR(255) PRIMARY KEY, 
    sdate VARCHAR(255), 
    stime VARCHAR(255), 
    duration VARCHAR(255), 
    repeatition VARCHAR(255), 
    interval_ VARCHAR(255), 
    edate VARCHAR(255), 
    etime VARCHAR(255)
)

CREATE TABLE job_queue_table (
    appid VARCHAR(255) PRIMARY KEY
)
```

### Deployment: Application Instance

```sql
CREATE TABLE deploy (
    appinstanceid VARCHAR(255) PRIMARY KEY, 
    username VARCHAR(255), 
    appid VARCHAR(255), 
    sdate VARCHAR(255), 
    stime VARCHAR(255), 
    duration int, 
    repeatation VARCHAR(5), 
    intervaltime int, 
    algonum int
)

CREATE TABLE Deployment_manager_db (
    Job_ID VARCHAR(32), 
    App_instance_ID VARCHAR(45), 
    Server_address VARCHAR(36), 
    App_run_type VARCHAR(36)
)
```

### Node-Manager Database

```sql
CREATE TABLE nodes (
    ip VARCHAR(255) NOT NULL, 
    port VARCHAR(255) NOT NULL, 
    status VARCHAR(255) NOT NULL, 
    user VARCHAR(255) NOT NULL, 
    PRIMARY KEY(ip,port)
)
```