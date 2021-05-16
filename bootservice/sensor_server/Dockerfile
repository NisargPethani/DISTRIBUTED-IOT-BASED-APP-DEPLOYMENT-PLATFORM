FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD kafka_topic.py sensor_temp.py sensor_biometric.py sensor.py sensor_light.py sensor_instance_id.py heart_beat_client.py sensor.sh pass sensor1.py sensor2.py sensor_server.py sensor_gps.py ./
ADD configuration ./configuration 
CMD ["python", "-u","sensor_server.py"]