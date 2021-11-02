# Install Docker Machine in VM


## Docker Machine Install

```bash
docker-machine create --driver generic \
					  --generic-ip-address $IP_ADDR \
					  --generic-ssh-key ~/.ssh/id_rsa \
					  --generic-ssh-user=$USERNAME $VM_NAME
```

---

## Docker Login

```bash
sudo docker login -u $DOCKERHUB_ID
```

---

## While Loop Syntax

```bash
while IFS= read -r line; 
do
	echo $line
done < provisioned_vms.txt
```

IFS : Internal field separator