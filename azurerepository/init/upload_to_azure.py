import os
import json
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareFileClient

def read_json_repo(filepath):
    f = open (filepath, "r")

    # Reading from file
    data = json.loads(f.read())
    
    c_str = data["c_str"]
    s_name = data["s_name"]

    return c_str, s_name
    # filepathrepo = "configuration/repo_config.json"
    # c_str, s_name = read_json_repo(filepathrepo)

def helper_copy_dir(source_dir, desti_dir, c_str, s_name, useless_ele, space = ""):
    for ele in os.listdir(source_dir):
        if ele in useless_ele:
            continue

        print(space, int(os.path.isdir(source_dir + "/" + ele)), ele)

        if os.path.isdir(source_dir + "/" + ele):
            dir_client = ShareDirectoryClient.from_connection_string(conn_str=c_str, share_name=s_name, directory_path=desti_dir + "/" + ele)
            dir_client.create_directory()

            helper_copy_dir(source_dir + "/" + ele, desti_dir + "/" + ele, c_str, s_name, useless_ele, space = space + "   ")
        else:
            file_client = ShareFileClient.from_connection_string(conn_str=c_str, share_name=s_name, file_path=desti_dir + "/" + ele)

            with open(source_dir + "/" + ele, "rb") as source_file:
                file_client.upload_file(source_file)

def upload_source(source_name, source_dir, desti_dir, c_str, s_name, useless_ele = {"__pycache__"}, space = ""):

    if os.path.isdir(source_dir + "/" + source_name):
        dir_client = ShareDirectoryClient.from_connection_string(conn_str=c_str, share_name=s_name, directory_path=desti_dir + "/" + source_name)
        dir_client.create_directory()

        print(source_dir + "/" + source_name)
        helper_copy_dir(source_dir + "/" + source_name, desti_dir + "/" + source_name, c_str, s_name, useless_ele, space = space)
    
    else:
        file_client = ShareFileClient.from_connection_string(conn_str=c_str, share_name=s_name, file_path=desti_dir + "/" + source_name)

        with open(source_dir + "/" + source_name, "rb") as source_file:
            file_client.upload_file(source_file)

    print("Upload Complete")


# filepathrepo = "configuration/repo_config.json"
# c_str, s_name = read_json_repo(filepathrepo)

# source_name = "app_copy"
# source_dir = "repository/apps_info"
# desti_dir = "repository/apps_info"

# upload_source(source_name, source_dir, desti_dir, c_str, s_name, useless_ele = {"__pycache__"}, space="   ")
