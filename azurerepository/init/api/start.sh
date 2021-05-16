
python3 $2/docker_file_generator.py $1 $2 $3
sudo docker container rm container_$1 
sudo docker image rm $1
sudo docker build --tag $1 $2
sudo docker run --net=host --name container_$1 $1 

# TO stop a running container sudo docker stop container_12345
