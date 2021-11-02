# Monitoring

## Heart Beat Producer

```cpp
def start_heart_beat():

    thread = threading.Thread(target=heart_beat)
    thread.start()
```

**Topic Name**

- Node
    
    ```cpp
    node_ip = get('https://api.ipify.org').text
    
    topic_name = "{}-{}_{}".format("node",node_ip, "8004")
    ```
    
- Application
    
    ```cpp
    topic_name = "{}-{}".format("application", App_instance_id)
    ```
    
- Service
    
    ```cpp
    topic_name = "{}-{}".format("service", service_name)
    ```
    

```cpp
heart_beat = "1"
producer.send(topic_name, heart_beat)
```

---

## Heart Beat Consumer

```python
threading.Thread(target=receive_reg_dereg_request).start()
```

**Register & Deregister**

- Service, Node & Application will register themselves dynamically on event.

```cpp
def receive_reg_dereg_request():

	reg_dereg_topic = 'register_deregister'
	for message in consumer:
		
		if request_type == 'register':
			register(request_msg)
		else:	
			deregister(request_msg)
```

- **Register**
    - Indirectly Start Listening heart-beat coming from That node/ Application/ Service on new thread.
    
    ```python
    def register(request_msg):
    
    	# request_msg --> Topic Name (Described in Heart Beat Producer)
    	
    	threading.Thread(
			target=heart_beat_consumer, 
			args=(topic_name)
    	).start()
    ```
    
- **Deregister**
    
    ```python
    # Applicable Only to Applications
    # Remove from Database
    ```
    

**Heart Beat Consumer**

```python
def heart_beat_consumer(topic_name):
	consumer = KafkaConsumer(
					topic_name, 
					['{}:{}'.format(kafka_ip, kafka_port)], 
					consumer_timeout_ms = 16000
				)
	
	for message in consumer:
		pass

	inform_fault_tolerance(topic_name)
```

```cpp
def	inform_fault_tolerance(topic_name):

	service_name = "Node/ Service/ App_instance_ID"
	topic_name = "monitoring"
	
	producer.send(topic_name, service_name)
```