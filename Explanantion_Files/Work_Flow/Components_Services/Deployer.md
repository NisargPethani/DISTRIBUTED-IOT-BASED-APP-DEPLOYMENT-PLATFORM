# Deployer

## Working

---

## Start Command

Socket Connection With node Manager
    
- **Requests for Node list**
    - **Stand Alone Node**
    - **Shared Node**
    
    ```python
    def request_nodes(msg_type, main_client_sock) :
        if(msg_type == "shared") :
                msg = "deployer node_list"
        else :
                msg = "deployer new_node"

        main_client_sock.send(msg.encode())
    ```
      
        
- **Calculate Load & Find best Possible Node to deploy Application**
    - **Get Statistics**
        
        `ssh_util class`
        
        ```python
        class ssh_util():
        
            def connect(self):
            "Login to the remote server"
        				
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
            """Execute a command on the remote host.Return a tuple containing
            an integer status and a two strings, the first containing stdout
            and the second containing stderr from the command."""
        
                if self.connect():
                    stdin, stdout, stderr = self.client.exec_command(
                                                command,
                                                timeout=10
                                            )

                self.ssh_output = stdout.read()
        ```
        
        `ssh_ret_val` contains All statistics about particular node 
        
        ```python
        ssh_util_obj = ssh_util()
        ssh_ret_flag, ssh_ret_val = ssh_util_obj.execute_command(
                                        ["vmstat -s"], 
                                        vm_ip, 
                                        username
                                    )
        
        total_memory = ssh_ret_val
        used_memory = ssh_ret_val
        ```
        
    - **Get Statistics**
        
        ```python
        ssh_ret_flag, ssh_ret_val = ssh_util_obj.execute_command(
        
            ["echo $[100-$(vmstat 1 2|tail -1|awk '{print $15}')]"], 
            vm_ip, 
            username
        )
        
        cpu_usage = ssh_ret_val
        ```
        
    - **Calculate Load**
        
        ```python
        def calculate_load(used_memory,total_memory, cpu_usage):
        
            ram_usage = used_memory/total_memory * 100
            load = (2 * cpu_usage * ram_usage) / (cpu_usage + ram_usage) 
            
            return load
        ```
            
- **Perform Operation on Best Node**
    - **Run app**
        
        ```python
        def perform_action_app( selected_node_addr, app_instance_id, 
        												app_run_type, kill = False) :
        	
            file_path = get_application_file_path(app_instance_id)
    
            msg = "start_app:" + app_instance_id + \
                        ":bash " + file_path + \
                        " " + app_instance_id + \
                        " " + file_path.rsplit('/',1)[0]
    
            client_sock.send(msg.encode()) 
        ```
            
- **DB Update**
    - **Insert `Application_Instance_Id` to DB**
        
        ```python
        job_id = uuid.uuid4()
        db_util.insert_into_db(
            job_id, app_instance_id, selected_node_addr, app_run_type	
        )
        ```
        

---

## **Kill Command**
    
- **Deregister `app_instance_id` to heart beat manager**
    - **Deregister Process**
        
        ```python
        deregister_to_heart_beat_manager(app_instance_id) 
        ```
        
        ```python
        def deregister_to_heart_beat_manager(application_instance_id):
            request_type = 'deregister'
            message = "{} {}-{}".format(
                                    request_type, 
                                    "application", 
                                    application_instance_id
                                )

            topic_name = "register_deregister"
            producer.send(topic_name, message.encode())
        ```
            
- **Kill Command Send to Node**
    
    ```python
    msg = "kill_app:" + app_instance_id
    client_sock.send(msg.encode())
    ```