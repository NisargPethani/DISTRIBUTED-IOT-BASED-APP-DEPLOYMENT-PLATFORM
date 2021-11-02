# Kafka Boot-Strapping

## SSH into VM

```bash
sshpass -f pass ssh -o StrictHostKeyChecking=no $USERNAME@$IP_ADDR $COMMAND
```

- **COMMAND**
    - Install JRE
        
        ```bash
        sudo apt install -y default-jre;
        ```
        
    - Download & Extract Kafka
        
        ```bash
        wget https://mirrors.estointernet.in/apache/kafka/2.8.0/kafka_2.13-2.8.0.tgz;
        tar -xzf kafka_2.13-2.8.0.tgz; 
        ```
        
    - Configuration Update
        
        ```bash
        python3 kafka_params_updater.py $IP_ADDR; 
        ```
        
        `.py` file has been transferred to VM before executing the command
        
        `kafka_params_updater.py`
        
        ```bash
        if line.startswith("#advertised.listeners") :
            line = line.replace("your.host.name", VM_IP)
            line = line.replace("#", "")
        ```
        
    - Start **ZooKeeper** & **Kafka Server**
        
        ```bash
        bin/zookeeper-server-start.sh -daemon config/zookeeper.properties;
        ```
        

---

## Transfer python file to VM

```bash
scp ./kafka_params_updater.py $USERNAME@$IP_ADDR:/home/$USERNAME
```