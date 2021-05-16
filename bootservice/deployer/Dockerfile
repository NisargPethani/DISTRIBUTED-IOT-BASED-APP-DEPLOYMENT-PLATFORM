FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD test.py deployer.py heart_beat_client.py vm_stat.sh load_balancer.py pass db_utility.py helper_file.py ./
ADD configuration ./configuration 
CMD ["python", "-u","deployer.py"]