import shutil
import os
import json

dir = [
    "../ui/repository/sensor_instance_info", 
    "../ui/repository/sensor_type_info", 
    "../ui/repository/controller_instance_info", 
    "../ui/repository/controller_type_info", 
    "../ui/repository/apps_info"]

############################################################# 
for i in dir:
    try:
        shutil.rmtree(i)
    except Exception:
        pass

    os.mkdir(i)

############################################################# 

try:
    shutil.rmtree("../ui/temp/")
except Exception:
    pass