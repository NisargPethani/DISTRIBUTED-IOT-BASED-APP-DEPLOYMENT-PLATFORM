from kafka import KafkaProducer
from json import loads
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10, 1))
message = 'stop:1141'
producer.send('appmanager_schedular', json.dumps(message).encode('utf-8'))
producer.flush()
producer.close()
print('messgae sent:',message)