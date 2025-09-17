Run Server
==============================

* Create Docker Network
    * Containers on the same network can communicate with each other by their container name.

```
docker network create my-app-network
```

* Build Server Docker Image

```
docker build --build-arg SERVER_PORT={SERVER_PORT} -t server_env -f Dockerfile.server .
```

* Run Server Docker Container 

```
docker run --rm --name {SERVER_HOSTNAME} --network my-app-network -p {SERVER_PORT}:{SERVER_PORT} server_env
```


Run Client
==============================

* Build Client Docker Image

```
docker build --build-arg SERVER_HOSTNAME={SERVER_HOSTNAME} --build-arg SERVER_PORT={SERVER_PORT} -t client_env -f Dockerfile.client .
```

* Run Client Docker Container 

```
docker run --rm --network my-app-network client_env
```

