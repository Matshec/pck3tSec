$image_name = "malw"
$container_name = "backend"
$network_name = "malnet"

docker build -t $image_name .
docker stop $container_name
docker rm $container_name
Set-Location api
docker run --cap-add=NET_ADMIN --name $container_name --network $network_name -p 8123:8000 --mount source=db,target=/app/api/db $image_name
Set-Location ..