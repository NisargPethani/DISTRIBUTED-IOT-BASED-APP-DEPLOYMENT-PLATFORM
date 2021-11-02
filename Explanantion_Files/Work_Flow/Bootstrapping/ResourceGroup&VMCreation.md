# Resource Group & VM Creation

## Azure Login

```bash
az login
```

---

## Azure Resource Group Creation

```bash
az group create --name $RESOURCE_GROUP_NAME --location centralindia
```

---

## VM Creation

```bash
Command :
az vm create  --resource-group $RESOURCE_GROUP_NAME \
			  --name $vm_name \
			  --image UbuntuLTS \
			  --output json \
			  --verbose \
			  --authentication-type all\
			  --generate-ssh-keys\
			  --admin-password Abc@12345xyz\
			  --query 'publicIpAddress' -o json

Return value : 
`PUBLIC_IP_ADDRESS`
```

---

## Port

```bash
az vm open-port --port 80 \
				--resource-group $RESOURCE_GROUP_NAME \
				--name $vm_name \
				--priority 600
```

---

## SSH Password Setup Using SSH

```bash
sshpass -f pass ssh -o StrictHostKeyChecking=no $USERNAME@$IP "sudo apt-get update; sudo apt-get install sshpass"
```