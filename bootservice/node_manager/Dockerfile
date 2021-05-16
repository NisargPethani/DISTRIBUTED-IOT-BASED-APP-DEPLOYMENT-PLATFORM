FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD node_manager_database_init.py heart_beat_client.py node_db_queries.py pass node_manager.py ./
ADD configuration ./configuration 
CMD ["python", "-u","node_manager.py", "0.0.0.0", "10000"]