# Hello There
![Basci Tests](https://github.com/Matshec/pck3tSec/workflows/Basci%20Tests/badge.svg)

## how to run all
```
 docker  network create nazwa-sieci
 docker run --cap-add=NET_ADMIN --name backend --network nazwa-sieci  -p 8123:8000 matshec/psec-hub:latest
 docker run --network nazwa-sieci -p 81:80  patrykzygmunt/pck3tsec-ui
```
and access ui interface at http://localhost:81

## DEV runs below 

## how to run frontend:
`> npm install`

`> npm start`

## how to run api server
`> ./manage.py runserver`

## how to  run core
`> sudo python runcore.py`

## how to run docker backend
`> docker run --cap-add=NET_ADMIN -p 8123:8000 matshec/psec-hub`

## Tests

### how to run critical tests
note that critical test can  only be run in docker

`> docker run --cap-add=NET_ADMIN matshec/psec-hub runtests_critical eth0`

### how to run api tests
`> cd api; ./manage.py test`

### how to run unittest
 `> PYTHONPATH="$PWD/api"; python -m unittest discover -s core/tests -p "*tests.py"`


