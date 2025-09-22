#!/bin/bash
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/server.key -out certs/server.crt \
  -subj "/C=KR/ST=Seoul/L=Seoul/O=Test/OU=Dev/CN=localhost"
