#!/bin/bash
temp="****************"
echo $temp
USERNAME=$1
IP_ADDR=$2
file_name="vm_stat.txt"
echo "Requesting node stats......."
#get VM stats in a file
vm_stat_command="vmstat -s"
cpu_stat_command="echo $[100-$(vmstat 1 2|tail -1|awk '{print $15}')]"
sshpass -f pass ssh -o StrictHostKeyChecking=no $USERNAME@$IP_ADDR "$vm_stat_command; $cpu_stat_command" > $file_name
echo "Received node Stats"