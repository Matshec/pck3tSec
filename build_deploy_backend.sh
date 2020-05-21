#!/bin/bash
image_name="malw2"
container_name="backend"
network_name="malnet"
echo $image_name
echo $network_name
echo $container_name
docker build -t $image_name .
docker stop $container_name || echo 'Container not working'
docker rm $container_name || echo 'Container not existing'
#docker run --cap-add=NET_ADMIN --name backend --network malnet -p 8123:8000 malw
