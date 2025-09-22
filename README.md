Run Server
==============================

<details>
<summary>Server Execution Procedure</summary>
      
1. Create Docker Network in Server
    * Containers on the same network can communicate with each other by their container name.
    * Docker's built-in DNS server automatically resolves container names to their internal IP addresses.

```
# E.g. {NETWORK_NAME}=test_network
docker network create {NETWORK_NAME}
```

2. Build Server Docker Image

```
# E.g. {SERVER_PORT}=8001
docker build --build-arg SERVER_PORT={SERVER_PORT} -t server_env -f Dockerfile.server .
```

3. Run Server Docker Container 

```
# E.g. {DOCKER_NAME}=test_server, {SERVER_PORT}=8001, {NETWORK_NAME}=test_network
export PUBLIC_IP=$(curl -s ifconfig.me)
docker run --rm -d --name {DOCKER_NAME} -p {SERVER_PORT}:{SERVER_PORT} --network {NETWORK_NAME} -e PUBLIC_IP=$PUBLIC_IP server_env
```

4. Check Real-Time Logs

```
# E.g. {DOCKER_NAME}=test_server
docker logs -f {DOCKER_NAME}
```

</details>


Run Client
==============================

<details>
<summary>Client Execution Procedure</summary>
      
1. Create Docker Network in Client
    * Containers on the same network can communicate with each other by their container name.
    * Docker's built-in DNS server automatically resolves container names to their internal IP addresses.

```
# E.g. {NETWORK_NAME}=test_network
docker network create {NETWORK_NAME}
```

2. Build Client Docker Image

```
# E.g. {SERVER_IP}=Public IP of Server (192.0.0.1), {SERVER_PORT}=8001
docker build --build-arg SERVER_HOSTNAME={SERVER_IP} --build-arg SERVER_PORT={SERVER_PORT} -t client_env -f Dockerfile.client .
```

3. Run Client Docker Container 

```
# E.g. {DOCKER_NAME}=test_server, {NETWORK_NAME}=test_network
docker run --rm -d --name {DOCKER_NAME} --network {NETWORK_NAME} client_env
```

</details>


Run Server with Nginx Proxy for HTTPS Server (Self-Signed Certificate)
==============================

<details>
<summary>Nginx Proxy Server Execution Procedure for HTTPS Server</summary>

1. Generate Self-Signed Certificate

```
bash generate-self-signed-cert.sh
```

2. Run Docker Compose

```
docker-compose -f self-signed-docker-compose.yml up --build
```

3. Turn-off Docker Compose

```
docker-compose down && docker compose up --build
```

</details>


Run Server with Nginx Proxy for HTTPS Server (Official Certificate)
==============================

<details>
<summary>Nginx Proxy Server Execution Procedure for HTTPS Server</summary>

1. Domain Setup
   * If you don't have a domain, use [DuckDNS](https://www.duckdns.org/). (e.g. test.duckdns.org)

2. Check Public IP

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

</details>
