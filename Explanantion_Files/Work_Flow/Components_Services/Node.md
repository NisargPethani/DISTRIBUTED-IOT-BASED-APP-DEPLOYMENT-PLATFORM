# Node

## Working
---

## Interaction with Node Manager

- Node Registration
    
    ```python
    sockt.connect((node_manager_ip, node_manager_port))
    request = "node " + ip + " "+str(port)
    sockt.sendall(request.encode())
    ```
    
---

## Start Application

- **Run Application**
    
    ```python
    def run_the_application(application_id,command_to_run_app):
    		
        download_app(application_id) // From Asure Repository
        os.system(command_to_run_app)		
    ```
    

- **Command To Run Application**:
    
    ```bash
    bash path_of_start.sh app_instance_id app_id algorithm_no
    ```
    
     
    
    - `start.sh`
        
        ```bash
        python3 $2/docker_file_generator.py $1 $2 $3
        sudo docker container rm container_$1 
        sudo docker image rm $1
        sudo docker build --tag $1 $2
        sudo docker run --net=host --name container_$1 $1
        ```
        
    - `Dockerfile`
        
        ```docker
        FROM python:3
        COPY platform_requirements.txt ./
        RUN pip install --no-cache-dir -r platform_requirements.txt
        ADD api_files ./
        CMD ["python", "-u","application.py", "app_instance_id", "algorithm_no"]
        ```
        
---

## Kill Application

- **Stop Application**
    
    ```python
    def stop_application(application_id):
        stop_application_command = "sudo docker stop container_{}".format(application_id)
        os.system(stop_application_command)
    ```