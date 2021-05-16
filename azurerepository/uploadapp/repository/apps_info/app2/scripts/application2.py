import interface_to_get_data_new
import action_and_notification_api

import sys
import time

#sensor_data = interface_to_get_data.get_sensor_data(0,'app_instance_63546eef86f64aec98c58e3ca96c38b3')
#sensor_data_stream = interface_to_get_data.get_stream_data(0, 'app_instance_63546eef86f64aec98c58e3ca96c38b3', 10)
#print(f'stream data: ')
#for data in sensor_data_stream:
#    print(data)

#action_and_notification_api.send_notification("Chal ja Bhagwan!")
#app_id = 5

while True:
	AC1 = interface_to_get_data_new.get_sensor_data(0,sys.argv[1])
	#AC2 = get_sensor_data(1,app_id)
	#AC3 = get_sensor_data(2,app_id)
	#AC4 = get_sensor_data(3,app_id)

	Total_temp = (AC1[0] + 500)
	threshold = 50
	if(threshold<Total_temp):
	    action_and_notification_api.send_notification("High temperature detected!")
	else:
	    action_and_notification_api.send_notification("Low temperature detected!")
	
	time.sleep(5)
