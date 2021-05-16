from kafka import KafkaConsumer, KafkaProducer
import json
import load_balancer as lb
import socket
import db_utility as db_util
import uuid
PORT = 10000
import json
import heart_beat_client
from requests import get
import threading 
from helper_file import ssh_util


print()
print()
print()
print()
print("*******************************************************************")
print("Deployer:", get('https://api.ipify.org').text)
print("*******************************************************************")
print()
print()
print()
print()
print()

MAIN_CLIENT_SOCKET=None

#get node manager port and ip
def get_nm_ip() :
	f = open('configuration/services_config.json', 'r')
	data = json.loads(f.read())
	node_manager_ip = data['node_manager']['ip']
	return node_manager_ip


#get kafka ip and port  
def getKafka_credentials():
    f = open ('configuration/kafka_config.json', "r")
    data = json.loads(f.read())
    ip = (data['ip'])
    port = str(data['port'])
    return ip,port

#Does exactly what it says
def deregister_to_heart_beat_manager(application_instance_id): ## deregister
	request_type = 'deregister'
	print("\n----------------De-registration with Heart Beat Manager---------------------\n")
	kafka_ip, kafka_port = getKafka_credentials()
	topic_name = "register_deregister"

	message = "{} {}-{}".format(request_type, "application", application_instance_id)
	print("Application {} message : {}\n".format(request_type,message))

	producer = KafkaProducer(bootstrap_servers = ['{}:{}'.format(kafka_ip, str(kafka_port))], 
	api_version = (0,10,1))
	print("Topic name :",topic_name)
	producer.send(topic_name, json.dumps(message).encode('utf-8'))

#run the docker container on the node : 
def run_container(app_instance_id, selected_node_addr) :
	ssh_util_obj = ssh_util()
	container_id = "container_{}".format(app_instance_id)
	vm_ip = (selected_node_addr.split())[0]
	username = db_util.get_node_username(selected_node_addr)
	ssh_ret_flag, ssh_ret_val = ssh_util_obj.execute_command(["sudo docker container start {}".format(container_id)], vm_ip, username)
	print("Flag and SSH Output :", ssh_ret_val )
	if(ssh_ret_flag) :	
		print("\nApplication started again successfully.....\n")
	else :
		print("\nError running application again on the same node....\n")
	



#get the path of application file from databse 
def get_application_file_path(app_instance_id):
	app_id = db_util.get_app_id(app_instance_id)
	file_path = "/".join([".", "repository", "apps_info", app_id, "scripts", "start.sh"])
	return file_path


#Send request to node manager for active nodes list 
#If the msg_type is shared --- ask node manager for node list
#If the msg_type is standalone ---- ask node manager for new node
def request_nodes(msg_type, main_client_sock) :
	if(msg_type == "shared") :
		msg = "deployer node_list"
	else :
		msg = "deployer new_node"
	main_client_sock.send(msg.encode())


#get response back from node manager 
#repsonse type : multiple;<ip> <port> <username> : <ip> <port> <username> 
def get_back_nodes(main_client_sock) :
	response = main_client_sock.recv(1024).decode()
	print("\n------------Node Manager Response-------------\n")
	print("Response from node manager :", response)
	response_type = (response.split(";"))[0]
	active_nodes_list = ((response.split(";"))[1]).split(":")
	print(f"Response Type : {response_type}\n")
	print(f"Active Nodes List : {active_nodes_list}\n")
	
	if(response_type == "single") :
		selected_node = active_nodes_list[0]
	else :
		node_index = lb.get_best_node(active_nodes_list)
		selected_node = active_nodes_list[node_index]

	return selected_node



#run app using sockets  
def perform_action_app(selected_node_addr, app_instance_id, app_run_type, kill = False) :
	#create a client socket 
	ip_add = (selected_node_addr.split())[0]
	port = int((selected_node_addr.split())[1])
	

	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client_sock.connect((ip_add, port))
	except Exception as e :
		print("Exception...", e)
		return
		# raise SystemExit(f"Connection failed : {e}")


	#kill the app - 
	if(kill) :
		msg = "kill_app:" + app_instance_id
		print("Inside Kill App:", msg)

		deregister_to_heart_beat_manager(app_instance_id)
		client_sock.send(msg.encode()) 

	#start running the app - 
	else :
		print("\n------------Results after load balancing-------------\n")
		print(f"Selected Node's IP Addr : {ip_add}\n")
		print(f"Selected Node's Port : {port}\n")

		#get init file from database :
		file_path = get_application_file_path(app_instance_id)
		msg = "start_app:" + app_instance_id + ":bash " + file_path + " " + app_instance_id + " " + file_path.rsplit('/',1)[0]
		client_sock.send(msg.encode()) 

		# Add data into db
		job_id = (str(uuid.uuid4()).replace('-', ''))
		db_util.insert_into_db(job_id, app_instance_id, selected_node_addr, app_run_type)
		
			

def main() : 

	#start the heartbeat client
	print("\n------------Deployment Manager Started-------------\n")

	#create a consumer for receiving app_ids from scheduler
	ip, port = getKafka_credentials()
	consumer_scheduler = KafkaConsumer('run_application_topic', bootstrap_servers=[ip + ':' + port],api_version=(0,10))


	#retrieve msg from scheduler :
	for message in consumer_scheduler :
		print("\n------------Scheduler Request-------------\n")
		response = json.loads(message.value).split()
		response_type = response[0]
		app_instance_id = response[-1]
		app_run_type = response[1]
		print(f"Response Type : {response_type}\n")
		print(f"App Instance ID : {app_instance_id}\n")
		print(f"App Run Type : {app_run_type}\n")
		print("Response type flag :", response_type == "kill")

		try:
			
			if(response_type == "kill" or "kill" in response_type) :
			
				#get the node id from database
				return_flag, selected_node_addr = db_util.get_server_address(app_instance_id)
				print("Inside COnsumer KILL if \n\n\n")
				if return_flag:
					perform_action_app(selected_node_addr , app_instance_id, app_run_type, True)
				else:
					print("Kill commnad not executed.... No record found with given info")
					continue

			else :
				#request nodes from node manager :
				MAIN_CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				try:
					node_manager_ip = get_nm_ip()
					MAIN_CLIENT_SOCKET.connect((node_manager_ip, PORT))
				except Exception as e :
					print("Eception...", e)
					continue
					# raise SystemExit(f"Connection failed : {e}")

				request_nodes(app_run_type, MAIN_CLIENT_SOCKET)

				#get back nodes list from node manager : 
				selected_node =  get_back_nodes(MAIN_CLIENT_SOCKET)
				selected_node_addr = selected_node.split()[0]
				selected_node_addr += " " + selected_node.split()[1]

				#run the app using sockets:
				perform_action_app(selected_node_addr, app_instance_id, app_run_type, False)

		except Exception as err:
			print()
			print("Exception while handing request.... ")
			print(err)
			print()
			continue	



#handle fault tolerance of app/node : 
def fault_tolerance() :
	#create a consumer for receiving app_ids from scheduler
	ip, port = getKafka_credentials()
	consumer_ft = KafkaConsumer('restart_app', bootstrap_servers=[ip + ':' + port],api_version=(0,10))
	for message in consumer_ft :
		try : 
			app_instance_id = json.loads(message.value)

			print("\n------------App Fault Tolerance Message-------------\n")
			print(f"App instance to be run again : {app_instance_id}")

			#get the node on which the app was running : 
			return_flag, selected_node_addr = db_util.get_server_address(app_instance_id)

			#if valid node address is returned : 
			if(return_flag) :
				node_status = db_util.get_node_status(selected_node_addr)

				#run on the same node : 
				if(node_status == "free" or node_status == "active") :
					print("Node is free/active... Running the app on same node again....")
					run_container(app_instance_id, selected_node_addr)

				#run on a different node : 
				else :
					
					return_status, app_run_type = db_util.get_app_run_type(app_instance_id)
					print("App run type and Return status :", app_run_type, return_status)
					if not return_status:
						print("\nUnable to retrieve app run type from database....\n")
					else:
						print("Requesting node manager for a new node to run the app")
						#global MAIN_CLIENT_SOCKET
						MAIN_CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						try:
							node_manager_ip = get_nm_ip()
							MAIN_CLIENT_SOCKET.connect((node_manager_ip, PORT))
						except Exception as e :
							print("Eception...", e)
							continue
						# raise SystemExit(f"Connection failed : {e}")

						print("Main Client Socker:", MAIN_CLIENT_SOCKET)
						request_nodes(app_run_type, MAIN_CLIENT_SOCKET)

						#get back nodes list from node manager : 
						selected_node =  get_back_nodes(MAIN_CLIENT_SOCKET)
						selected_node_addr = selected_node.split()[0]
						selected_node_addr += " " + selected_node.split()[1]

						#run the app using sockets:
						perform_action_app(selected_node_addr, app_instance_id, app_run_type, False)


			#if a valid node address is not returned : 
			else :
				print("Error retrieving node address for the stopped app....")


		except Exception as err:
			print()
			print("Exception while handing request.... ")
			print(err)
			print()
			continue	


if __name__ == "__main__" :
	#main()
	thread1 = threading.Thread(target=main)
	thread1.start()
	thread2 = threading.Thread(target=fault_tolerance)
	thread2.start()
	heart_beat_client.start_heart_beat()
