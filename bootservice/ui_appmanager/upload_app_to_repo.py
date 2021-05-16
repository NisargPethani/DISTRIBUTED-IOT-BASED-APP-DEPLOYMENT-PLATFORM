import os
import json
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareFileClient
import upload_to_azure

def read_json_repo(filepath):
    f = open (filepath, "r")

    # Reading from file
    data = json.loads(f.read())
    
    c_str = data["c_str"]
    s_name = data["s_name"]

    return c_str, s_name
    # filepathrepo = "configuration/repo_config.json"
    # c_str, s_name = read_json_repo(filepathrepo)

def upload_app(app_id):

    filepathrepo = "configuration/repo_config.json"
    c_str, s_name = read_json_repo(filepathrepo)

    source_name = app_id
    source_dir = "repository/apps_info"
    desti_dir = "repository/apps_info"

    useless_ele = {"__pycache__", "platform_requirements.txt","kafka_config.json","start.sh","interface_to_get_data_new.py","db_config.json","action_and_notification_api.py","docker_file_generator.py"}
    upload_to_azure.upload_source(source_name, source_dir, desti_dir, c_str, s_name, useless_ele=useless_ele)
