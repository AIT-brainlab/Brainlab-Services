FROM nvidia/cuda:11.6.0-devel-ubuntu20.04

# https://vsupalov.com/docker-arg-env-variable-guide/
# https://bobcares.com/blog/debian_frontendnoninteractive-docker/
ARG DEBIAN_FRONTEND=noninteractive
# Timezone
ENV TZ="Asia/Bangkok"
ENV http_proxy "http://192.41.170.23:3128"
ENV https_proxy "http://192.41.170.23:3128"

# like CD command in terminal. it will create directory if path is not existed
WORKDIR /root
RUN apt update && apt upgrade -y
# Set timezone
RUN apt install -y tzdata
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

EXPOSE 80 443 8000

RUN apt install python3 python3-pip python3-dev -y
RUN apt install git -y
RUN apt install curl -y

RUN apt install npm -y
RUN npm install -g configurable-http-proxy

RUN pip3 install jupyter_server
RUN pip3 install jupyterlab
RUN pip3 install jupyterhub
RUN pip3 install pipenv

# basic tools
RUN apt install wget vim telnet iputils-ping -y
RUN apt install cron rsync sudo -y
RUN /bin/bash -c -l 'crontab -u root -l; echo "0 * * * * /root/sync.sh" | crontab -u root -'


COPY ./etc_host/passwd /etc/passwd
COPY ./etc_host/group /etc/group
COPY ./etc_host/shadow /etc/shadow

# cert
RUN apt install python3 python3-venv libaugeas0 -y
RUN pip install certbot

# COPY ./root/new-cert.sh /root/new-cert.sh
# COPY ./root/start.sh /root/start.sh
COPY ./root/jupyterhub_config.py /root/jupyterhub_config.py
# RUN /root/start.sh
CMD jupyterhub -f /root/jupyterhub_config.py
# CMD tail -f /dev/null
# CMD /root/start.sh &> start.log