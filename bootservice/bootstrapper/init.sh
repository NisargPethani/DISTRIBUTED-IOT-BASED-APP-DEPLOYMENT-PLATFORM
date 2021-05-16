#!/bin/bash

printf "\n\n"
echo "### Initialising bootstrap process....."
printf "\n\n"

#list of scripts(path to scripts) to run : 
declare -a scripts_list=(
# "install_prereqs.sh"     #Install prerequisites 
# "provision_vms.sh"          #Provision VMs on azure and save IPs and other info
# "install_vm_clients.sh"     #Install docker and components on every VM
"create_vm_mappings.py"     #Assign a VM to each service
"copy_configs.sh"           #Copy configuration files to each service
"kafka_bootstrap.sh"        #Bootstrap Kafka
"monitoring_bootstrap.sh"
"scheduler_bootstrap.sh"    #Bootstrap scheduler
"ui_appmanager_bootstrap.sh"
"deployer_bootstrap.sh"     #Bootstrap deployer
"sensor_server_bootstrap.sh"
"controller_server_bootstrap.sh"
"node_manager_bootstrap.sh"
"fault_tolerence_bootstrap.sh"
)

for i in "${!scripts_list[@]}"
do

  #retrieve element from the list : 
  a=${scripts_list[$i]}

  #check if the file exists : 
  if [ ! -f "$a" ]; then
    echo "$a doesn't exist."
    exit 1
  fi

  #check the file extension : 
  ext="$(echo $a | cut -d'.' -f2)" 
  #run the file according to the extension :
  if [ $ext == "sh" ]; then 
	bash $a

  elif [ $ext == "py" ]; then 
	python $a
  fi
done
