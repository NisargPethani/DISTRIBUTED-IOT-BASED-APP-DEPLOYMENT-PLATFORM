from requests import get
import json
import os
from zipfile import ZipFile

##################################################################### Dict
controller_dict = {
    "controller_type": None,
    "controller_location": {
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

##################################################################### controller controller_type
controller_type = "controller_type_BUZZER"
controller_save_dir_name = "BUZZER_controller"

os.mkdir(controller_save_dir_name)

##################################################################### Controller controller_location
####################################### port info
port_start = 50631
port_jump = 1

####################################### ip info
ip = ""
# get('https://api.ipify.org').text

##################################################################### controller geo_location
room_no = "-1"
house_no = "-1"
street = "UNK"
city = "HYD"

##################################################################### Json Creation
####################################### controller count
number_of_controller = 5

####################################### make json
curr_port = port_start

for i in range(number_of_controller):
    ################## controller controller_type
    controller_dict['controller_type'] = controller_type

    ################## Controller controller_location
    #### port info
    port = str(curr_port)

    controller_dict['controller_location']['port'] = port
    curr_port += port_jump

    #### ip info
    controller_dict['controller_location']['ip'] = ip

    ################## controller geo_location
    controller_dict['geo_location']['room_no'] = room_no
    controller_dict['geo_location']['house_no'] = house_no
    controller_dict['geo_location']['street'] = street
    controller_dict['geo_location']['city'] = city

    ################## JSON
    filename = os.path.join(controller_save_dir_name, "controller_instance_{}.json".format(i+1))
    with open(filename, 'w') as jsonfile:
        json.dump(controller_dict, jsonfile, indent=4)


##################################################################### Zip Creation
zipfilename = "controller_instance_configuration.zip"

zipfilepath = os.path.join(controller_save_dir_name, zipfilename)
with ZipFile(zipfilepath, 'w') as zipfile:
    for i in range(number_of_controller):
        filename = os.path.join(controller_save_dir_name, "controller_instance_{}.json".format(i+1))
        zipfile.write(filename)

