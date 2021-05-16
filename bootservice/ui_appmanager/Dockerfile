FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD app_validator.py sensor_type_validator.py sensor_instance_validator.py controller_type_validator.py upload_to_azure.py deploy_validator.py ui_appmanager.py heart_beat_client.py pass helper.py upload_app_to_repo.py controller_instance_validator.py ./
ADD templates ./templates 
ADD configuration ./configuration 
ADD repository ./repository 
CMD ["python", "-u","ui_appmanager.py"]