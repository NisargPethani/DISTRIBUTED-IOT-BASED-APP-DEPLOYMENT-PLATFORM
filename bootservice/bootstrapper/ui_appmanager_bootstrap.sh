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


    if [ "$SERVICE" = "ui_appmanager" ]; then
      break
    fi
done < provisioned_vms.txt
echo $VM_NAME
printf "\n\n"
echo "#### Deploying ui_appmanager at VM $IP_ADDR ####"
printf "\n\n"
gnome-terminal --title="UI & App Manager" -e "bash -c \
\"cd ..; \
printf \"********************************************************\"; \
echo ---------------------- ui_appmanager -------------------------; \
printf \"********************************************************\"; \
./start.sh ui_appmanager ui_appmanager; \
eval \$(docker-machine env ${VM_NAME}); \
docker run --net=host --name container_ui_appmanager username/ui_appmanager; \
bash\""
