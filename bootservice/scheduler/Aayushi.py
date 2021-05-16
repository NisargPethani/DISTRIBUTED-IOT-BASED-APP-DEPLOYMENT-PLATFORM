from kafka import KafkaConsumer
from json import loads
import json

consumer = KafkaConsumer('run_application_topic',bootstrap_servers=['localhost:9092'],api_version=(0, 10))

for message in consumer:
    print(message.value)