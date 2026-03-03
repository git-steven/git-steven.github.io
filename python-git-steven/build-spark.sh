#!/bin/bash
docker image rm -f terracoil/spark
docker --log-level debug build --progress=plain --no-cache --platform linux/amd64 -t terracoil/spark  .
