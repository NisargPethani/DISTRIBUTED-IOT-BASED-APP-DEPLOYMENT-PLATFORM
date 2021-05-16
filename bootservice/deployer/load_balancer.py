import random
import json
import os
from helper_file import ssh_util


def get_load(username,vm_ip) :
    #temp file to store putput of bash commands 
    stat_file = "vm_stat.txt"

    #execute bash file to extract VM stats
    # os.system(f"bash vm_stat.sh {username} {vm_ip}")

    ssh_util_obj = ssh_util()
    ssh_ret_flag, ssh_ret_val = ssh_util_obj.execute_command(["vmstat -s"], vm_ip, username)

    if ssh_ret_flag:            
        print("Starts Found successfully...")
    else:
        print("Stats not found....")
        raise NotImplementedError

    with open(stat_file, "wb") as f:
        f.write(ssh_ret_val)

    #retrieve cpu usage and memory usage from 
    with open(stat_file, "r") as f:
        stats = f.readlines()


    total_memory = (stats[0].strip().split())[0]
    used_memory = (stats[1].strip().split())[0]


    ssh_util_obj = ssh_util()
    ssh_ret_flag, ssh_ret_val = ssh_util_obj.execute_command(["echo $[100-$(vmstat 1 2|tail -1|awk '{print $15}')]"], vm_ip, username)

    if ssh_ret_flag:            
        print("Starts Found successfully...")
    else:
        print("Stats not found....")
        raise NotImplementedError

    cpu_usage = ssh_ret_val
    # os.system(f"rm {stat_file}")
    return calculate_load(int(used_memory), int(total_memory), int(cpu_usage))


#get CPU PERCENTAGE OF VM for last one hour
'''os.system("az vm monitor metrics tail --name VM1 -g team1 --metric \"Percentage CPU\" > metrics.json")
with open("metrics.json", "r") as f:
    data = json.loads(f.read())


x = data["value"]
data_size = len(x[0]["timeseries"][0]['data'])

#take latest average CPU %
for i in range(data_size-1,0,-1) :
    cpu_percentage = x[0]["timeseries"][0]['data'][i]['average']
    if(cpu_percentage) :
        break'''


def calculate_load(used_memory,total_memory, cpu_usage):
    ram_usage = used_memory/total_memory * 100
    load = (2 * cpu_usage * ram_usage) / (cpu_usage + ram_usage) 
    print("load is : ", load)
    return load


def get_best_node(nodes_list):
    min_index = len(nodes_list)
    min_load = 100
    for index in range(len(nodes_list)):
        parts = nodes_list[index].split()
        username = parts[-1]
        vm_ip = parts[0]
        load = get_load(username, vm_ip)
        if(load < min_load) :
            min_load = load
            min_index = index

    return min_index

