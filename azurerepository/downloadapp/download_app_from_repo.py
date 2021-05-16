import os
import json
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareFileClient
import download_from_azure
from distutils.dir_util import copy_tree

def read_json_repo(filepath):
    f = open (filepath, "r")

    # Reading from file
    data = json.loads(f.read())
    
    c_str = data["c_str"]
    s_name = data["s_name"]

    return c_str, s_name
    # filepathrepo = "configuration/repo_config.json"
    # c_str, s_name = read_json_repo(filepathrepo)

def download_api():

    filepathrepo = "configuration/repo_config.json"
    c_str, s_name = read_json_repo(filepathrepo)

    source_name = "api"
    source_dir = "repository"
    desti_dir = "repository"

    if os.path.exists(desti_dir + "/" + source_name):
        print("No need to download.... Dir/File already exixsts")
        return

    download_from_azure.download_source(source_name, source_dir, desti_dir, c_str, s_name, space="   ")

def download_app(app_id):

    filepathrepo = "configuration/repo_config.json"
    c_str, s_name = read_json_repo(filepathrepo)

    # pre work
    if os.path.exists("repository"):
        if os.path.exists("repository/apps_info"):
            pass
        else:
            os.mkdir("repository/apps_info")
    else:
        os.mkdir("repository")
        os.mkdir("repository/apps_info")

    # Actual App data download
    source_name = app_id
    source_dir = "repository/apps_info"
    desti_dir = "repository/apps_info"

    if os.path.exists(desti_dir + "/" + source_name):
        print("No need to download.... Dir/File already exixsts")
        return

    download_from_azure.download_source(source_name, source_dir, desti_dir, c_str, s_name, space="   ")

    # Api Download
    download_api()    

    # copy api files to application
    fromDirectory = "repository/api"
    toDirectory = desti_dir + "/" + app_id + "/" + "scripts"

    copy_tree(fromDirectory, toDirectory)

download_app("app2")

