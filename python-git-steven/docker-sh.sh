#!/bin/bash
docker run --platform linux/amd64 -v ./data:/data -it --entrypoint sh terracoil/spark
