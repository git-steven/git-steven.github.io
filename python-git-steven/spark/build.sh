#!/bin/bash
# docker compose down
docker image rm -f apache-spark.local:3.5.1
docker --log-level debug build --progress=plain --no-cache --platform linux/amd64 -t apache-spark.local:3.5.1 -f Dockerfile .
# docker-compose up