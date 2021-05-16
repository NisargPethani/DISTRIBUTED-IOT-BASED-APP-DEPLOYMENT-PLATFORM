import interface_to_get_data_new
import action_and_notification_api
import setController
import send_sms_api
from datetime import datetime
import threading
import sys
import time
import heart_beat_client

import a1
import a2
import a3

heart_beat_client.start_heart_beat()
def_arg = sys.argv[1]

AlgoNumber = 0
try:
    AlgoNumber = int(sys.argv[2])
except Exception:
    AlgoNumber = 0


####################################
def ALGO1():
    while True:
        time.sleep(5)
        a2.five_time_unit_iteration()

def ALGO2():
    while True:
        time.sleep(2)
        a1.two_time_unit_iteration()

def ALGO3():
    a3.buzzer_sound()

###################################

if AlgoNumber == 0:
    threading.Thread(target=ALGO1).start()

elif AlgoNumber == 1:
    threading.Thread(target=ALGO2).start()

else:
    threading.Thread(target=ALGO3).start()
