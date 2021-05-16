from requests import get
import json
import os
from zipfile import ZipFile
import sys
import shutil



##################################################################### Dict
sensor_dict = {
    "sensor_type": None,
    "sensor_location": {
        "ip": None,
        "port": None
    },
    "geo_location": {
        "room_no": None,
        "house_no": None,
        "street": None,
        "city": None
    }
}

##################################################################### sensor sensor_type
sensor_type = "sensor_type_{}".format(sys.argv[1])
sensor_save_dir_name = "{}_sensor".format(sys.argv[1])

shutil.rmtree(sensor_save_dir_name)

os.mkdir(sensor_save_dir_name)

##################################################################### sensor sensor_location
####################################### port info
port_start = int(sys.argv[2])
port_jump = 1

####################################### ip info
ip = get('https://api.ipify.org').text

##################################################################### sensor geo_location
room_no = "0"
house_no = "0"
street = "UNK"
city = "HYD"

##################################################################### Json Creation
####################################### sensor count
number_of_sensor = 5

####################################### make json
curr_port = port_start

for i in range(number_of_sensor):
    ################## sensor sensor_type
    sensor_dict['sensor_type'] = sensor_type

    ################## sensor sensor_location
    #### port info
    port = str(curr_port)

    sensor_dict['sensor_location']['port'] = port
    curr_port += port_jump

    #### ip info
    sensor_dict['sensor_location']['ip'] = ip

    ################## sensor geo_location
    sensor_dict['geo_location']['room_no'] = room_no
    sensor_dict['geo_location']['house_no'] = house_no
    sensor_dict['geo_location']['street'] = street
    sensor_dict['geo_location']['city'] = city

    ################## JSON
    filename = os.path.join(sensor_save_dir_name, "sensor_instance_{}.json".format(i+1))
    with open(filename, 'w') as jsonfile:
        json.dump(sensor_dict, jsonfile, indent=4)


##################################################################### Zip Creation
# zipfilename = sensor_save_dir_name+"/sensor_instance_configuration.zip"

# zipfilepath = os.path.join(sensor_save_dir_name, zipfilename)
# with ZipFile(zipfilename, 'w') as zipfile:
#     for i in range(number_of_sensor):
#         filename = os.path.join(sensor_save_dir_name, "sensor_instance_{}.json".format(i+1))
#         zipfile.write(filename)

