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


def get_two_time_unit_data():
    
    threadlist = []
    j=0

    for i in range(bus_count):
        t = threading.Thread(name="thread_{}_{}".format(i, j), target=get_specific_sensor_data, args=(i, j))
        threadlist.append(t)
        t.start()

    time.sleep(1)

    for i in range(bus_count):
        threadlist[i].join()

buzz_done = set()

def buzzer_sound():

    print("30 TIME UNIT ITERATIONS..........")

    # gps_sensor_infos = []
    
    get_two_time_unit_data()

    # for b in range(bus_count):
    #     sensor_data = interface_to_get_data_new.get_sensor_data( gps_sensor_start_index + b*4 , def_arg)
    #     gps_sensor_infos.append(sensor_data)

    for i in range(bus_count):

        bus_id = i

        x = gps_sensor_infos[i][0]
        y = gps_sensor_infos[i][1]

        curr_bus_info[i]["x"] = x
        curr_bus_info[i]["y"] = y

    for i in range(bus_count):
        for j in range(i+1, bus_count):
            for k in range(j+1, bus_count):

                x1 = curr_bus_info[i]["x"]
                x2 = curr_bus_info[j]["x"]
                x3 = curr_bus_info[k]["x"]

                y1 = curr_bus_info[i]["y"]
                y2 = curr_bus_info[j]["y"]
                y3 = curr_bus_info[k]["y"]

                cen_x = (x1 + x2 + x3) / 3
                cen_y = (y1 + y2 + y3) / 3

                d1 = pow(pow(x1-cen_x,2)+pow(y1-cen_y,2),0.5)
                d2 = pow(pow(x2-cen_x,2)+pow(y2-cen_y,2),0.5)
                d3 = pow(pow(x3-cen_x,2)+pow(y3-cen_y,2),0.5)

                print("##########################", d1, d2, d3, 2)

                max_d = max( max(d1, d2) , d3 )

                if max_d < 2:
                    if j in buzz_done:
                        pass
                    else:
                        buzz_done.add(j)
                    
                        final_msg = tym() + "Buzzer for BusID: {}".format(j)

                        # print(final_msg)

                        threading.Thread(target=setController.set_controller_data, args=(j*3 + controller_start + buzzer_controller_start_index, "ON", def_arg,)).start()
                        threading.Thread(target=action_and_notification_api.send_notification, args=(final_msg,)).start()

                    if k in buzz_done:
                        pass
                    else:
                        buzz_done.add(k)
                    
                        final_msg = tym() + "Buzzer for BusID: {}".format(k)

                        # print(final_msg)

                        threading.Thread(target=setController.set_controller_data, args=(k*3 + controller_start + buzzer_controller_start_index, "ON", def_arg,)).start()
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
