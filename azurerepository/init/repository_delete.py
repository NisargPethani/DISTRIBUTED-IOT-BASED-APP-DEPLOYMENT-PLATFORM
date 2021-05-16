from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareFileClient
import json

def read_json_repo(filepath):
    f = open (filepath, "r")

    # Reading from file
    data = json.loads(f.read())
    
    c_str = data["c_str"]
    s_name = data["s_name"]

    return c_str, s_name
    # filepathrepo = "configuration/repo_config.json"
    # c_str, s_name = read_json_repo(filepathrepo)

def delete_dir_tree(c_str, s_name, d_name, space = ""):

    dir_client = ShareDirectoryClient.from_connection_string(conn_str=c_str, share_name=s_name, directory_path=d_name)

    my_list = []
    for item in dir_client.list_directories_and_files():
        my_list.append(item)

    for ele in my_list:
        print(space, ele)

        if ele['is_directory']:
            delete_dir_tree(c_str, s_name, d_name+"/"+ele['name'], space = space+"   ")
        else:
            file_client = ShareFileClient.from_connection_string(conn_str=c_str, share_name=s_name, file_path=d_name+"/"+ele['name'])
            file_client.delete_file()

    dir_client.delete_directory()

filepathrepo = "configuration/repo_config.json"
c_str, s_name = read_json_repo(filepathrepo)

d_name = "repository"

print(d_name)
delete_dir_tree(c_str, s_name, d_name, space="   ")