#!/bin/bash

while IFS= read -r line; 
do
    IP_ADDR="$(echo $line | cut -d' ' -f1)" 
    #removing '' from IP_ADDR
    IP_ADDR="${IP_ADDR%\'}"
    IP_ADDR="${IP_ADDR#\'}"

    VM_NAME="$(echo $line | cut -d' ' -f2)"
    VM_NAME="${VM_NAME%\'}"
    VM_NAME="${VM_NAME#\'}"

    USERNAME="$(echo $line | cut -d' ' -f3)"
    USERNAME="${USERNAME%\'}"
    USERNAME="${USERNAME#\'}"

    SERVICE="$(echo $line | cut -d' ' -f4)"
    SERVICE="${SERVICE%\'}"
    SERVICE="${SERVICE#\'}"


    if [ "$SERVICE" = "node_manager" ]; then
      break
    fi
done < provisioned_vms.txt

while IFS= read -r line; 
do
  DOCKER_USERNAME=$line
done < docker_creds.txt

echo $VM_NAME
printf "\n\n"
echo "#### Deploying node_manager at VM $IP_ADDR ####"
printf "\n\n"
gnome-terminal --title="Node manager" -e "bash -c \
\"cd ..; \
printf \"********************************************************\"; \
echo ---------------------- node_manager -------------------------; \
printf \"********************************************************\"; \
./start.sh node_manager node_manager; \
eval \$(docker-machine env ${VM_NAME}); \
docker run --net=host --name container_node_manager ${DOCKER_USERNAME}/node_manager; \
bash\""

# sudo docker container rm container_node_manager;\
# sudo docker image rm ${DOCKER_USERNAME}/node_manager;\ 
