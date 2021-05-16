# #!/bin/bash
INDEX=1

while IFS= read -r line; 
do
temp="${line%\"}"
temp="${temp#\"}"
# ssh $USERNAME@$temp "sudo curl -L 'https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)' -o /usr/local/bin/docker-compose; sudo chmod +x /usr/local/bin/docker-compose; exit"
done < provisioned_vms.txt

while IFS= read -r line; 
do
    
    # exit
    # docker-machine create \
    # --driver generic \
    # --generic-ip-address $temp\
    # --generic-ssh-key ~/.ssh/id_rsa \
    # --generic-ssh-user=akshat
    # vm

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
    
    printf "\n\n"
    echo "#### Trying to connect to $VM_NAME at $IP_ADDR ####"
    printf "\n\n"
    docker-machine create --driver generic --generic-ip-address $IP_ADDR --generic-ssh-key ~/.ssh/id_rsa --generic-ssh-user=$USERNAME $VM_NAME
done < provisioned_vms.txt

echo "Enter dockerhub id"
read DOCKERHUB_ID
echo "$DOCKERHUB_ID" >> docker_creds.txt
sudo docker login -u $DOCKERHUB_ID
