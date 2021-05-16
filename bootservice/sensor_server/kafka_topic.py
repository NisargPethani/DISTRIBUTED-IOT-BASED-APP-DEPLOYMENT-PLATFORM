from kafka.admin import KafkaAdminClient, NewTopic
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

def create_topic(id):
    
    filepath = "configuration/kafka_config.json"
    kafka_ip, kafka_port = read_json_kafka(filepath)
    
    admin_client = KafkaAdminClient(bootstrap_servers="{}:{}".format(kafka_ip, kafka_port), client_id='Aviral')
    topic_list = []
    topic_list.append(NewTopic(name=id, num_partitions=1, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)