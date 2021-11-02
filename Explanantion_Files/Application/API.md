# API

## Notification API

- **UI Notification**
    
    ```python
    def send_notification(app_instance_id):
    
        notif_message = appname + ":" + " " + notif_message   
        
        username, appname = getappnameandusername(app_instance_id)
        topic_name = username
    
        producer.send(topic_name, json.dumps(notif_message).encode('utf-8'))
    ```
    
- **Message Notification**
    
    ```python
    def send_email(message):
    
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
    
        s.login("sender_email", "password")
        s.sendmail("sender_email", "receiver_email", message)
    
        s.quit()
    ```
    
---

## Fetch Sensor Data API

- **Non Streaming Data**
    
    ```python
    def get_sensor_data(sensor_idx, app_instance_id):
    
        sensor_id = sensor_idx_to_id_map(sensor_idx, app_instance_id)
        topic_name = sensor_id
      
        consumer = KafkaConsumer(
            topic_name, 
            bootstrap_servers = ['{}:{}'.format(kafka_ip,kafka_port)], 
            api_version = (0,10)
        )
    
        for message in consumer:
            sensor_data = message.value.decode()
            return sensor_data
    ```
    
- **Streaming Data**
    
    ```python
    def get_stream_data(sensor_idx, app_instance_id, number_of_data_points):
    
        sensor_id = sensor_idx_to_id_map(sensor_idx, app_instance_id)
        topic_name = sensor_id
      
        consumer = KafkaConsumer(
            topic_name, 
            bootstrap_servers = ['{}:{}'.format(kafka_ip,kafka_port)], 
            api_version = (0,10)
        )
    
        sensor_data_list = []
        i=0
    
        for message in consumer:
            if(i==number_of_data_points):
                break
      
            sensor_data = ast.literal_eval(sensor_data)
            sensor_data_list.append(sensor_data)
            
            i+=1
    
        return sensor_data_list
    ```
    
---

## Set Controller Data API

```python
def set_controller_data(controller_idx, message_to_controller, app_instance_id):

    controller_id = controller_idx_to_id_map(controller_idx, app_instance_id)
    topic_name = controller_id
    
    producer.send(topic_name, message_to_controller.encode('utf-8'))
```