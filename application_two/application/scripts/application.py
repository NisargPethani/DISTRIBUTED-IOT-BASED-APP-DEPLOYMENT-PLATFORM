import interface_to_get_data_new
import action_and_notification_api
import setController
import send_sms_api
import heart_beat_client
import threading
import sys
import time

heart_beat_client.start_heart_beat()
def_arg = sys.argv[1]


print()
print("*************************Inside app")

while True:
	AC1 = interface_to_get_data_new.get_sensor_data(0,def_arg)
	
	Total_temp = AC1[0]
	threshold = 50
	if(threshold<Total_temp):
		setController.set_controller_data(0,"OFF", def_arg)

		message = "High temperature detected!... Received Temptature: " + str(AC1[0])
		
		threading.Thread(target=action_and_notification_api.send_notification, args=(message, ))
		threading.Thread(target=send_sms_api.send_sms, args=(message, ))
		threading.Thread(target=send_sms_api.send_email, args=(message, ))
	else:
		setController.set_controller_data(0,"ON", def_arg)

		message = "Low temperature detected!... Received Temptature: " + str(AC1[0])
		
		threading.Thread(target=action_and_notification_api.send_notification, args=(message, ))
		threading.Thread(target=send_sms_api.send_sms, args=(message, ))
		threading.Thread(target=send_sms_api.send_email, args=(message, ))

	time.sleep(5)
