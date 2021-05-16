import json 

#list contaning name of services
services = [
	"kafka", 
	"scheduler", 
	"Deployer", 
	"Sensor_manager", 
	"ui_appmanager", 
	"node_manager",
	"fault_tolerence",
	"monitoring",
	"sensor_server",
	"controller_server"
]    


print('\n\n##################################')
print('### Allocating VMS to services ### ')
print('##################################\n\n')

with open("provisioned_vms.txt", "r") as f:
	lines = f.readlines()
open('provisioned_vms.txt', 'w').close() # This line clears the contents of file.

data = {}       #data to be written to json file
count = 0
num_vms = len(lines)
flag = False
for i in services :
	parts = lines[count].split()
	ip = parts[0].strip("'")
	vm_name = parts[1].strip("'").rstrip("\n")
	username = parts[2].strip("'")
	service_name = i.lower()
	data[service_name] = {}
	data[service_name].update({
	    'ip': ip,
	    'username': username,
	    'vm_name': vm_name
		})
	if service_name == "kafka":
		data[service_name]['port']=9092
	
	# add name of the service attached to VM in provisioned_vms file
	with open("provisioned_vms.txt", "a") as f:
		line = lines[count].rstrip("\n") + " '" + service_name + "'\n" 
		f.write(line)
	count = (count + 1) % num_vms


with open('./final_config/services_config.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
with open('./final_config/kafka_config.json', 'w') as outfile:
    json.dump(data['kafka'], outfile, indent=4)

print('### VMS alloted to services ###\n ')






		




