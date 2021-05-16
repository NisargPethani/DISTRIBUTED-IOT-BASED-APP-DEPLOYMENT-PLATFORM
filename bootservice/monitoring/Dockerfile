FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD monitoring.py heart_beat_client.py pass service_names.txt ./
ADD configuration ./configuration 
CMD ["python", "-u","monitoring.py"]