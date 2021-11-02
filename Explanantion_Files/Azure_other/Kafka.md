# Kafka

## Producer

```python
address = '{}:{}'.format(kafka_ip,kafka_port)
producer = KafkaProducer(bootstrap_servers=[address],api_version=(0,10,1))

producer.send("topic_name",send_str.encode())
```

---

## Comsumer

```python
address = '{}:{}'.format(kafka_ip,kafka_port)
consumer = KafkaConsumer('topic_name',bootstrap_servers=[address],api_version=(0, 10))

for message in consumer:
    msg = message.value.decode()
    print('msg:',msg)   
```