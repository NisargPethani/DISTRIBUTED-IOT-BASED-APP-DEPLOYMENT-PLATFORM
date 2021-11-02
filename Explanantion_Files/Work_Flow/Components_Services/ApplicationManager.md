# Application Manager

**IMP** : Does **Validation** in each component

---

- **Signup, Login & Logout**
- **Notification**
- **Fetch All available Notifications**
    
    
    ```python
    ip_port = '{}:{}'.format(kafka_ip,kafka_port)
    
    consumer = KafkaConsumer(
		bootstrap_servers = [ip_port], 
		api_version = (0,10),
		consumer_timeout_ms = 1000, 
		auto_offset_reset="earliest"
    )
      
    username = session['username_user']
    partition = TopicPartition(username, 0)
    
    consumer.assign([partition])
    consumer.seek(partition, 0)
    
    notification_string = ""    
    
    for message in consumer:
        notification_string += str(message.value) + "<br>"
    ```
    

- **Sensor & Controller Type/ Instance Registration**
- **App Upload**
- **App Deploy**
- **Sensor Binding**
    
    
    ```python
    def getsensorinstaceid(	sentype, locroom,lochouse,locstreet,loccity, alerdytaken ):
    	
		wherequery = 	"sensor_type_id='"+sentypeuuid+ \
						"' and loc_room="+str(locroom)+ \
						" and loc_house="+str(lochouse)+ \
						" and loc_street='"+locstreet+ \
						"' and loc_city='"+loccity+"'"
    		
		sql = "SELECT id FROM sensorinstance where "+wherequery
		
		myresult = mycursor.fetchall()
		
		idlist = []
		for i in myresult:
			idlist.append(i[0])
		
		for i in idlist:
			if i not in alerdytaken:
				return True, i
    ```