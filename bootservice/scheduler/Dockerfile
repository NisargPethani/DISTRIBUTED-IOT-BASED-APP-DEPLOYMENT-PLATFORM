FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD createHeap.py heart_beat_client.py scheduler.py Aayushi.py pass scheduler_init.py scheduler_items.py pethani.py ./
ADD configuration ./configuration 
CMD ["python", "-u","scheduler.py"]