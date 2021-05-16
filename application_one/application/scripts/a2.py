import interface_to_get_data_new
import action_and_notification_api
import setController
import send_sms_api
from datetime import datetime
import threading
import sys
import time
import heart_beat_client


def_arg = sys.argv[1]

############################################# Predefined

bus_count = 5

barricades = {
    "North":(0.5,1.5),
    "South":(-0.5,0.5)
}

#######

# bus0 : gps, temp, light, biometric

gps_sensor_start_index = 0
temp_sensor_start_index = 1
light_sensor_start_index = 2
bimetric_sensor_start_index = 3

light_controller_start_index = 0
ac_controller_start_index = 1
buzzer_controller_start_index = 2

controller_start = 0


#######

# bus0 : gps, temp, light, biometric ------------ 0 - 3
# bus1 : gps, temp, light, biometric ------------ 4 - 7
# bus2 : gps, temp, light, biometric ------------ 8 - 11
# bus3 : gps, temp, light, biometric ------------ 12 - 15
# bus4 : gps, temp, light, biometric ------------ 16 - 19


# bus0 : light, ac, buzzer ------------ 0 - 2
# bus1 : light, ac, buzzer ------------ 3 - 5
# bus2 : light, ac, buzzer ------------ 6 - 8
# bus3 : light, ac, buzzer ------------ 9 - 11
# bus4 : light, ac, buzzer ------------ 12 - 14

# barricades : 20 - 21
# iiit : 22


############################################# Functions

curr_bus_info = {
    0 : {
        "x" : None,
        "y" : None,
        "lux" : None,
        "ac" : None,
        "pass" : None
    },
    1 : {
        "x" : None,
        "y" : None,
        "lux" : None,
        "ac" : None,
        "pass" : None
    },
    2 : {
        "x" : None,
        "y" : None,
        "lux" : None,
        "ac" : None,
        "pass" : None
    },
    3 : {
        "x" : None,
        "y" : None,
        "lux" : None,
        "ac" : None,
        "pass" : None
    },
    4 : {
        "x" : None,
        "y" : None,
        "lux" : None,
        "ac" : None,
        "pass" : None
    },
}

def tym():
    now = datetime.now()
    
    tym = "{}: ".format(now)
    return tym


def bigger(x,y):
    if(x>=y):
        decider = "x"
    else:
        decider = "y"
    return decider

def check(bus_id,x2,y2):
    for barr in barricades:
        x1 = barricades[barr][0]
        y1 = barricades[barr][1]
        
        if(pow(pow(x1-x2,2)+pow(y1-y2,2),0.5)<=1):
            send_sms_api.send_email(bus_id,barr)
            return False
    return True

gps_sensor_infos = [None,None,None,None,None]
light_sensor_infos = [None,None,None,None,None]
temp_sensor_infos = [None,None,None,None,None]
biometric_sensor_infos = [None,None,None,None,None]

def get_specific_sensor_data(busid, sensor_type):

    sensor_data = interface_to_get_data_new.get_sensor_data( sensor_type + busid*4 , def_arg)

    if sensor_type == 0:
        gps_sensor_infos[busid] = sensor_data
    elif sensor_type == 1:
        temp_sensor_infos[busid] = sensor_data[0]
    elif sensor_type == 2:
        light_sensor_infos[busid] = sensor_data[0]
    elif sensor_type == 3:
        biometric_sensor_infos[busid] = sensor_data[0]



def calculate_fare(bus_id):
    x = curr_bus_info[bus_id]["x"]
    y = curr_bus_info[bus_id]["y"]

    fare = (pow(pow(x,2)+pow(y,2),0.5)) * 20
    return fare


def get_five_time_unit_data():

    len = 3
    threadlist = []

    for i in range(bus_count):
        for j in range(1, 1+len):
            t = threading.Thread(name="thread_{}_{}".format(i, j), target=get_specific_sensor_data, args=(i, j))
            threadlist.append(t)
            t.start()

    time.sleep(1)

    for i in range(bus_count):
        for j in range(1, 1+len):
            threadlist[i*len + (j-1)].join()

def five_time_unit_iteration():

    print("FIVE TIME UNIT ITERATIONS..........")

    ########### DATA COLLECTION PART
    get_five_time_unit_data()
    

    ########### ACTION PART
    # [biometric_id]

    for i, val in enumerate(biometric_sensor_infos):

        bus_id = i
        bimetric_info = val

        curr_bus_info[bus_id]["pass"] += 1

        message_part1 = "Person (PersonID: {}) is boarding at Location ({}, {}) in BusID: {}".format(bimetric_info, curr_bus_info[bus_id]["x"], curr_bus_info[bus_id]["y"], bus_id)

        message_part2 = "Fair: {}".format(calculate_fare(bus_id))

        final_msg = tym() + "\n" + message_part1 + "\n" + message_part2
        
        # print(final_msg)
        threading.Thread(target=send_sms_api.send_sms, args=(final_msg,)).start()
        threading.Thread(target=action_and_notification_api.send_notification, args=(final_msg,)).start()

        # send_sms_api.send_sms(final_msg)
        # action_and_notification_api.send_notification(final_msg)

    for i, val in enumerate(light_sensor_infos):

        bus_id = i
        light_info = light_sensor_infos[bus_id]

        if light_info < 300: # and curr_bus_info[bus_id]["lux"]==False:
            # print("******** LIGHT ON", light_info, curr_bus_info[bus_id]["lux"])

            curr_bus_info[bus_id]["lux"] = True

            final_msg = tym() + "Light ON of BusID: {}".format(bus_id)

            # print(final_msg)
            threading.Thread(target=setController.set_controller_data, args=(bus_id*3 + controller_start + light_controller_start_index, "ON", def_arg,)).start()
            threading.Thread(target=action_and_notification_api.send_notification, args=(final_msg,)).start()

            # setController.set_controller_data(bus_id, "ON", def_arg)
            # action_and_notification_api.send_notification(final_msg)
            
        
        if light_info > 700: # and curr_bus_info[bus_id]["lux"]==True:
            # print("******** LIGHT OFF", light_info, curr_bus_info[bus_id]["lux"])
            
            curr_bus_info[bus_id]["lux"] = False
            
            final_msg = tym() + "Light OFF of BusID: {}".format(bus_id)

            # print(final_msg)
            threading.Thread(target=setController.set_controller_data, args=(bus_id*3 + controller_start + light_controller_start_index, "OFF", def_arg,)).start()
            threading.Thread(target=action_and_notification_api.send_notification, args=(final_msg,)).start()

            # setController.set_controller_data(bus_id, "OFF", def_arg)
            # action_and_notification_api.send_notification(final_msg)

    
    for i, val in enumerate(temp_sensor_infos):

        bus_id = i
        temp_info = temp_sensor_infos[bus_id]

        if temp_info > 60: # and curr_bus_info[bus_id]["ac"] == False:
            # print("******** AC ON", temp_info, curr_bus_info[bus_id]["ac"])

            curr_bus_info[bus_id]["ac"] = True
            
            final_msg = tym() + "AC ON of BusID: {}".format(bus_id)

            # setController.set_controller_data(bus_id, "ON", def_arg)
            # action_and_notification_api.send_notification(final_msg)
            
            # print(final_msg)
            threading.Thread(target=setController.set_controller_data, args=(bus_id*3 + controller_start + ac_controller_start_index, "ON", def_arg,)).start()
            threading.Thread(target=action_and_notification_api.send_notification, args=(final_msg,)).start()
        
        if temp_info < 40: # and curr_bus_info[bus_id]["ac"]==True:
            # print("******** AC OFF", temp_info, curr_bus_info[bus_id]["ac"])

            curr_bus_info[bus_id]["ac"] = False
            
            final_msg = tym() + "AC OFF of BusID: {}".format(bus_id)

            # setController.set_controller_data(bus_id, "OFF", def_arg)
            # action_and_notification_api.send_notification(final_msg)

            # print(final_msg)

            threading.Thread(target=setController.set_controller_data, args=(bus_id*3 + controller_start + ac_controller_start_index, "OFF", def_arg,)).start()
            threading.Thread(target=action_and_notification_api.send_notification, args=(final_msg,)).start()

def prework():

    len = 4
    threadlist = []

    for i in range(bus_count):
        for j in range(len):
            t = threading.Thread(name="thread_{}_{}".format(i, j), target=get_specific_sensor_data, args=(i, j))
            threadlist.append(t)
            t.start()

    time.sleep(1)

    for i in range(bus_count):
        for j in range(len):
            threadlist[i*len + j].join()

    for i in range(bus_count):
        curr_bus_info[i]['x'] = gps_sensor_infos[i][0]
        curr_bus_info[i]['y'] = gps_sensor_infos[i][1]

    for i in range(bus_count):
        curr_bus_info[i]['lux'] = False
        curr_bus_info[i]['ac'] = False
        curr_bus_info[i]['pass'] = 0


prework()

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print(curr_bus_info)
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print()
print()
print()
print()
