FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD controller.py controller_server.py heart_beat_client.py pass port_script.sh controller.sh ./
ADD configuration ./configuration 
CMD ["python", "-u","controller_server.py"]