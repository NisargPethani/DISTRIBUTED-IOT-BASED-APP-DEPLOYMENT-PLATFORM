# Service Boot-Strapping

## Make docker-image for Service

```bash
start.sh service_dir service_name
```

- **`start.sh`**
    
    ```bash
    python3 $1/docker_file_generator.py $1 $2
    sudo docker container rm container_$1 
    sudo docker image rm $1
    cd $1
    sudo docker build --no-cache -t $DOCKER_USERNAME/$1 .
    sudo docker push $DOCKER_USERNAME/$1
    ```
    
    in line 1 `docker_file_generator.py` generates `Dockerfile`
    
- **`Dockerfile`**
    
    ```bash
    FROM python:3
    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt
    ADD deployer.py other_files ./
    ADD configuration ./configuration 
    CMD ["python", "-u","deployer.py"]
    ```
    

---

## Start Service on Remote Machine

```bash
eval \$(docker-machine env ${VM_NAME}); \
docker run --net=host \
           --name service_name username/serive_dir
```