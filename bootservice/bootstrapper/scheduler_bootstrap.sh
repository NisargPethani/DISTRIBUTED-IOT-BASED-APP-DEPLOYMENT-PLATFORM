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


    if [ "$SERVICE" = "scheduler" ]; then
      break
    fi
done < provisioned_vms.txt

while IFS= read -r line; 
do
  DOCKER_USERNAME=$line
done < docker_creds.txt

echo $VM_NAME
printf "\n\n"
echo "#### Deploying scheduler at VM $IP_ADDR ####"
printf "\n\n"
gnome-terminal --title="Scheduler" -e "bash -c \
\"cd ..; \
printf \"********************************************************\"; \
echo ---------------------- SCHEDULER -------------------------; \
printf \"********************************************************\"; \
./start.sh scheduler scheduler; \
eval \$(docker-machine env ${VM_NAME}); \
docker run --net=host --name container_scheduler ${DOCKER_USERNAME}/scheduler; \
bash\""
