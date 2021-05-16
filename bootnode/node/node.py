# start 
# node_manager pa register karna padaga.
# static - ip port static list ma daldenga.
# import functions
import socket
import threading
import sys
import os
import ctypes 
import json
from download_app_from_repo import *


#application_thread_map = {app_id: thread_id}
application_thread_map = {}
lock = threading.Lock()
queue = []

def get_node_manager_details(service_config_path):
	f = open (service_config_path, "r")
	data = json.loads(f.read())
	# kafka_ip = ""
	# kafka_port = "9092"

	node_manager_ip = data['node_manager']['ip']
	node_manager_port = data['node_manager']['port']
	return node_manager_ip, node_manager_port



def run_the_application(application_id,command_to_run_app):
    print("Application Id :", application_id)
    download_app(application_id)
    print("Start file request :", command_to_run_app)
    break_command = command_to_run_app.split()
    if break_command[0] != 'bash':
        print("command not valid")
        exit(0)    

    print(break_command[1])
    if os.path.isfile(break_command[1]):
        os.system(command_to_run_app)
    else:
        print("Not a valid file to run")    

# execute thw appp
# pas the argument app.

def stop_application(application_id):

    # thread_id = application_thread_map[application_id]
    # res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
    #           ctypes.py_object(SystemExit)) 
    # if res > 1: 
    #     ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
    #     print('Exception raise failure') 
    stop_application_command = "sudo docker stop container_{}".format(application_id)
    os.system(stop_application_command)


# stop the app.


# def server():
#     # threads pa listen
#     <start_app>:<application_id>:<command_to_execute> ## start the app.
#     <kill_app>:<application_id> # kill the app.
#     pass
def handle_request(connection, client_address):
    request = connection.recv(1024).decode()
    request_array = request.split(':')
    request_type = request_array[0]
    # identify the request ie from the client or the sensor_server
    try:
        if request_type == 'start_app':
            print("Request For : ", request_type)
            #arguments = request_array[1].strip(')').split('(')[1].split(',')
            application_id = request_array[1]
            command =  request_array[2]
            thread_id = threading.get_ident()
            application_thread_map.update({application_id: thread_id})
            run_the_application(application_id,command)
            """
            if len(arguments) > 2:
                connection.send("Invalid number of arguments provided, one expected.")
            else:
                sensor_id = int(arguments[0])
                # Acquire the lock before changing the queue.
                print("Client Request for data for sensor id : {}".format(sensor_id))

                lock.acquire()
                queue.append((connection, sensor_id))
                lock.release()
            """
        elif (request_type == 'kill_app'):
            application_id = request_array[1]
            stop_application(application_id)
            #connection.close()

    except AttributeError as error:
        print(error)
        connection.sendall(('Error :' + str(error)).encode())
    except TypeError as error:
        print(error)
        connection.sendall(('Error :' + str(error)).encode())


def server(server_ip, server_port):
    try:
        sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as error:
        print(error)
        exit(0)
    sockt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sockt.bind((server_ip, server_port))
        print('Socket is listening at ip : {}, port : {}'.format(server_ip, server_port))
        sockt.listen(10)

        while True:
            connection, client_address = sockt.accept()
            print("Got connection request from :{}".format(client_address))
            thread = threading.Thread(target=handle_request, args=(connection, client_address))
            thread.start()

    except socket.error as error:
        print(error)
    finally:
        sockt.close()


# Details of the node_manager host
# hostName = 'localhost'
# node_manager_ip = '52.172.135.44'
# node_manager_port = 10000

def client_connect(service_config_path):
    node_manager_ip, node_manager_port = get_node_manager_details(service_config_path)

    try:
        sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
    except socket.error as error:
        print("Socket creation failed with error :", error)
        sys.exit(0)
    connected = False
    while(not connected):
        try:
            sockt.connect((node_manager_ip, node_manager_port))
            request = "node " + ip + " "+str(port)
            sockt.sendall(request.encode()) 
            connected = True
        except socket.error as error:
            print(error)
            # connected = True
    # finally:
    print("Connected Successfully!!")
    sockt.close()

if __name__ == "__main__":
    
    service_config_path = "./configuration/services_config.json"
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    thread = threading.Thread(target=client_connect, args=([service_config_path]))
    thread.start()

    server(server_ip, server_port)

