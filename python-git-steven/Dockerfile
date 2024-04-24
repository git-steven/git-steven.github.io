FROM bitnami/spark:latest
COPY spark-defaults.conf /opt/bitnami/spark/conf/

RUN  venv/bin/pip install graphframes py4j

#FROM spark:3.5.1-scala2.12-java17-ubuntu
#
#USER root
#
#COPY spark-defaults.conf /opt/spark/conf/
#
#RUN set -ex; \
#    apt-get update; \
#    apt-get install -y python3 python3-pip; \
#    rm -rf /var/lib/apt/lists/*
#
#USER spark