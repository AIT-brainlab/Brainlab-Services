FROM akraradets/base-ubuntu:22.04

RUN apt update && apt upgrade -y
RUN apt install -y apache2

RUN apt install -y php libapache2-mod-php
RUN apt install -y composer
RUN apt install -y curl php-curl
RUN apt install -y php-ldap
RUN apt install -y php-xml


CMD tail -f /dev/null