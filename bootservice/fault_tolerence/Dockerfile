FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD fault_tolerence.py pass service_names.txt helper_file.py ./
ADD configuration ./configuration 
CMD ["python", "-u","fault_tolerence.py"]