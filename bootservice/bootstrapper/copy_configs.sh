#!/bin/bash

# ################# Service ##########################
declare -a services_list=(
"scheduler"
"ui_appmanager"
"deployer"
"fault_tolerence"
"node_manager"
"monitoring"
"sensor_server"
"controller_server"
)

for i in "${services_list[@]}"
do
    cp ./final_config/services_config.json ../$i/configuration/services_config.json
    cp ./final_config/db_config.json ../$i/configuration/db_config.json
    cp ./final_config/kafka_config.json ../$i/configuration/kafka_config.json
    cp ./final_config/repo_config.json ../$i/configuration/repo_config.json
    cp ./final_config/scheduler_db.json ../$i/configuration/scheduler_db.json    
    cp ./requirements.txt ../$i/requirements.txt
    cp ./pass ../$i/pass
done


# ################# Bootnode ##########################
declare -a node_list=(
"bootnode"
)

for i in "${node_list[@]}"
do
    cp ./final_config/services_config.json ../../$i/node/configuration/services_config.json
    cp ./final_config/db_config.json ../../$i/node/configuration/db_config.json
    cp ./final_config/kafka_config.json ../../$i/node/configuration/kafka_config.json
    cp ./final_config/repo_config.json ../../$i/node/configuration/repo_config.json
    cp ./final_config/scheduler_db.json ../../$i/node/configuration/scheduler_db.json    
    cp ./requirements.txt ../../$i/node/requirements.txt
    cp ./pass ../../$i/pass
done



# ################# Asure repository ##########################
declare -a arepo_list=(
"list"
"init"
"downloadapp"
"uploadapp"
)

for i in "${arepo_list[@]}"
do
    # cp ./final_config/services_config.json ../../azurerepository/$i/configuration/services_config.json
    # cp ./final_config/db_config.json ../../azurerepository/$i/configuration/db_config.json
    # cp ./final_config/kafka_config.json ../../azurerepository/$i/configuration/kafka_config.json
    cp ./final_config/repo_config.json ../../azurerepository/$i/configuration/repo_config.json
    # cp ./final_config/scheduler_db.json ../../azurerepository/$i/configuration/scheduler_db.json    
done


# ################# Asure Api repository ##########################
declare -a aapi_list=(
"api"
)

for i in "${aapi_list[@]}"
do
    # cp ./final_config/services_config.json ../../azurerepository/init/$i/services_config.json
    cp ./final_config/db_config.json ../../azurerepository/init/$i/db_config.json
    cp ./final_config/kafka_config.json ../../azurerepository/init/$i/kafka_config.json
    # cp ./final_config/repo_config.json ../../azurerepository/init/$i/repo_config.json
    # cp ./final_config/scheduler_db.json ../../azurerepository/init/$i/scheduler_db.json    
done


# ################# Asure database ##########################
declare -a adata_list=(
"prework"
"sqlconnector"
)

for i in "${adata_list[@]}"
do
    # cp ./final_config/services_config.json ../../azuredatabase/$i/configuration/services_config.json
    cp ./final_config/db_config.json ../../azuredatabase/$i/configuration/db_config.json
    # cp ./final_config/kafka_config.json ../../azuredatabase/$i/configuration/kafka_config.json
    # cp ./final_config/repo_config.json ../../azuredatabase/$i/configuration/repo_config.json
    cp ./final_config/scheduler_db.json ../../azuredatabase/$i/configuration/scheduler_db.json    
done
