import heapq
import datetime
import threading
from scheduler_items import *

def get_time(HH):
    return int(HH)

# def check_and_run():
#     cur_datetime = str(datetime.now())
#     cur_time = ((cur_datetime.split(' ')[1]).split('.'))[0]
#     hour, minute, second = cur_time.split(':')
    
#     if(str(start_heap[0].hour)==hour and str(start_heap[0].minute)==minute):
#         app = start_heap[0].uuid
#         job_queue.append(app)
#         print(job_queue)
#         heapq.heappop(start_heap)
#         #now send this app value to deployment manager
#         send_to_deployment_mgr(job_queue[-1])

class thisTime(object):
    def __init__(self, date_, hour, minute, uuid,  duration, interval):
        self.date_ = date_
        self.hour = hour
        self.minute = minute
        self.uuid = uuid
        self.duration = duration
        self.interval = interval

    def __lt__(self, other):
        # print("hh =>",self.hour,"other =>",  other.hour)
        if(self.date_ == other.date_):
            if(self.hour == other.hour):
                return self.minute < other.minute
            else:
                return self.hour < other.hour  
        else:
            self.date_ < other.date_

def create_heap(given_date, given_time, heap_name, uuid, duration="", interval=""):
    HH, MM = given_time.split(':')
    hour = get_time(HH)
    minute = get_time(MM)
    heapq.heappush(heap_name,thisTime(given_date, hour, minute, uuid, duration, interval))

    

def printHeap(heap_name):
    for obj in heap_name:
        print(obj.hour, obj.minute)


#get this info from app_manager
def start_app(start_date, start_time, end_date, end_time, app, duration, interval):
    create_heap(start_date, start_time, start_heap, app)
    create_heap(end_date, end_time, end_heap, app, duration, interval)
    print("heap created")
    print("****** starting times",app,"*********")
    printHeap(start_heap)
    print("Current Time:", datetime.datetime.now())
    print('*******************************')
    print("****** ending times",app,"*********")
    printHeap(end_heap)
    print('*******************************')

# printHeap(start_heap)