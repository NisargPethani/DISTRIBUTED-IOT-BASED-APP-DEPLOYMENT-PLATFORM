from azure.storage.fileshare import ShareDirectoryClient
import json
import upload_to_azure

def read_json_repo(filepath):
    f = open (filepath, "r")

    # Reading from file
    data = json.loads(f.read())
    
    c_str = data["c_str"]
    s_name = data["s_name"]

    return c_str, s_name

def create_repo_structure(d_name, sub_dirs):    
    
    filepathrepo = "configuration/repo_config.json"
    c_str, s_name = read_json_repo(filepathrepo)

    dir_client = ShareDirectoryClient.from_connection_string(c_str, s_name, d_name)

    print(d_name)
    dir_client.create_directory()

    for subd_name in sub_dirs:
        print("   ", subd_name)
        dir_client.create_subdirectory(subd_name)

def copy_necessory_files():
    filepathrepo = "configuration/repo_config.json"
    c_str, s_name = read_json_repo(filepathrepo)

    source_name = "api"
    source_dir = "."
    desti_dir = "repository"

    upload_to_azure.upload_source(source_name, source_dir, desti_dir, c_str, s_name, space="   ")

d_name = "repository"
sub_dirs = ["apps_info", "controller_instance_info", "controller_type_info", "sensor_instance_info", "sensor_type_info"]

create_repo_structure(d_name, sub_dirs)  
copy_necessory_files()