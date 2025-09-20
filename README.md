Run Server
==============================

<details>
<summary>Server Execution Procedure</summary>
      
1. Create Docker Network
    * Containers on the same network can communicate with each other by their container name.

```
docker network create {NETWORK_NAME}
```

2. Build Server Docker Image

```
docker build --build-arg SERVER_PORT={SERVER_PORT} -t server_env -f Dockerfile.server .
```

3. Run Server Docker Container 

```
docker run --rm server_env

or

docker run --rm --name {SERVER_HOSTNAME} server_env

or

# Using Docker Network
docker run --rm --name {SERVER_HOSTNAME} --network {NETWORK_NAME} server_env
```

</details>

Run Client
==============================

1. Build Client Docker Image

```
docker build --build-arg SERVER_HOSTNAME={SERVER_IP} --build-arg SERVER_PORT={SERVER_PORT} -t client_env -f Dockerfile.client .

or

docker build --build-arg SERVER_HOSTNAME={SERVER_HOSTNAME} --build-arg SERVER_PORT={SERVER_PORT} -t client_env -f Dockerfile.client .
```

2. Run Client Docker Container 

```
docker run --rm client_env

or

# Using Docker Network
docker run --rm --network {NETWORK_NAME} client_env
```


Run Server with Nginx Proxy
==============================

1. Domain Setup
   * If you don't have a domain, use [DuckDNS](https://www.duckdns.org/). (e.g. test.duckdns.org)

3. Check Public IP

```
curl ifconfig.me
nslookup {DOMAIN_NAME}
```

3. Run Docker Compose of Certbot service 

    * Docker Compose to run the Certbot service one time for the purpose of issuing a new SSL/TLS certificate

    * Command Breakdown
        * **`docker-compose run`**: Executes a one-time command for a service defined in `docker-compose.yml`.
        * **`--rm`**: Automatically removes the container after the command exits. Ideal for one-off tasks like issuing certificates.
        * **`--service-ports`**: Publishes the service's defined ports to the host. Necessary for Certbot to use port 80/443 for domain validation.
        * **`certbot`**: The name of the service to run.
        * **`certonly`**: A Certbot subcommand to obtain a certificate without automatically modifying web server configurations.

    * Certbot Options
        * **`-d {DOMAIN_NAME}`**: Specifies the domain name(s) to issue a certificate for.
        * **`--email {EMAIL_ADDRESS}`**: The email address for registration and certificate expiration notices.
        * **`--agree-tos`**: Agrees to the Let's Encrypt Terms of Service.
        * **`--no-eff-email`**: Opts out of sharing your email with the Electronic Frontier Foundation (EFF).

```
docker-compose run --rm --service-ports certbot certonly -d {DOMAIN_NAME} --email {EMAIL_ADDRESS}--agree-tos --no-eff-email
```
