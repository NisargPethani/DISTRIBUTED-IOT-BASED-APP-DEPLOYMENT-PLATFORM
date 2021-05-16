while IFS= read -r line; 
do
    DOCKER_USERNAME=$line
done < ./bootstrapper/docker_creds.txt

python3 $1/docker_file_generator.py $1 $2
sudo docker container rm container_$1 
sudo docker image rm $1
cd $1
sudo docker build --no-cache -t $DOCKER_USERNAME/$1 .
sudo docker push $DOCKER_USERNAME/$1
# sudo docker run --net=host --name container_$1 $1 

# TO stop a running container sudo docker stop container_12345
