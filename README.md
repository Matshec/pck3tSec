# Hello There
![Basci Tests](https://github.com/Matshec/pck3tSec/workflows/Basci%20Tests/badge.svg)

## how to run frontend:
`> npm install`

`> npm start`

## how to run api server
`> ./manage.py runserver`

## how to  run core
`> sudo python runcore.py`

## how to run critical tests
note that critical test can  only be run in docker

`> sudo python `

## how to run load tests

`> sudo python testing/traffic_test.py ${worker_threads_count} ${time_of_test_in_minutes}`

Load tests takes two parameters:
* ${worker_threads_count} defines threads count used to generate http requests to foreing hosts
* ${time_of_test_in_minutes} defines time for which http traffic will be generated

Load tests must be executed on same host as backend application is deployed

## how to run functional tests

`> sudo python testing/functional_tests.py ${api_url}`

Functional tests takes one parameter which defines REST api endpoint exposed by backend service. 
Functional tests must be execute on same host as backend application is deployed

## how to run docker
`> docker run --cap-add=NET_ADMIN -p 8124:8000 psec:debug`
```
 docker  network create nazwa-sieci
 docker run --network malnet -p 81:80  patrykzygmunt/pck3tsec-ui
 docker run --cap-add=NET_ADMIN --name backend --network malnet  -p 8123:8000 -it malw
```

docker is listening for http requests on localhost:8124

## additional scripts
### build_deploy_sript
Builds and runs backend image using docker
### run_functional_tests
Runs functional tests for backend application
### run_load_tests
Runs load tests for backend application

