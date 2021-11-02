# Fault Tollerance


## Application
- Again deploy Application as New Application

```cpp
topic_name = "restart_app"
producer.send(topic_name, app_instance_id)
```

---

## Node
    
```cpp
sockt.connect((node_manager_ip, node_manager_port))
request = "{} {} {}".format("fault_tolerance",node_ip, node_port)

sockt.sendall(request.encode())
```
    
---

## Service
    
```cpp
command = "sudo docker start container_{}".format(service_name)

ssh_object = ssh_util()
flag, ssh_output = ssh_object.execute_command(commands, vm_ip, vm_username)
```

```cpp
class ssh_util():
    def __init__(self):

        self.host= ""
        self.username = "aditya"
        self.password = "Abc@12345xyz"

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
                    hostname=self.host, 
                    username=self.username, 
                    password=self.password, 
                    allow_agent=False,
                    look_for_keys=False
                )    
        
    def execute_command(self,commands, vm_ip, vm_username):
            
        stdin, stdout, stderr = self.client.exec_command(command,timeout=10)
        self.ssh_output = stdout.read()
        self.ssh_error = stderr.read()
```