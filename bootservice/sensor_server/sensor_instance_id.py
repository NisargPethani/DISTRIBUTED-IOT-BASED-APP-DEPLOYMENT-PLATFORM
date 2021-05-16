from kafka import KafkaConsumer
import json

def read_json_kafka(filepath):
    f = open (filepath, "r")
  
    # Reading from file
    data = json.loads(f.read())

    ip = data["ip"]
    port = data["port"]

    return ip, port

    # filepath = "configuration/kafka_config.json"
    # kafka_ip, kafka_port = read_json_kafka(filepath)

def get_id():

    print("into Get id Fun")

    filepath = "configuration/kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepath)

    consumer = KafkaConsumer('appmanager_sensormanager',bootstrap_servers=['{}:{}'.format(kafka_ip, kafka_port)],api_version=(0, 10))

    for message in consumer:
        print('msg:',message.value)
        msg = message.value.decode()
        break

    return msg
