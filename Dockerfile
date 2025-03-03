FROM python:3.12.4-slim

# MAINTAINER Javier Cortés <javier@yeboyebo.es>

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y apt-utils build-essential vim tzdata libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev freetds-dev libgl1 libegl1 libxkbcommon-x11-0 libjpeg-dev libdbus-1-3 xcb libxcb-cursor0 libpq-dev libglib2.0-0
RUN apt-get install -y python3-anyjson

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /pineboo/
RUN mkdir /src/
RUN mkdir /src/app/
RUN mkdir /src/app/logs
RUN touch /src/app/logs/yebo.log
RUN chmod -R a+rw /src
RUN echo "COMPROBANDO PERMISOS /src"
RUN ls -la -R /src
RUN mkdir /static/
RUN mkdir /static/images/
RUN chmod -R a+rw /static
RUN mkdir /external/
WORKDIR /src/
ADD requirements.txt /src/
RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt --use-deprecated=legacy-resolver
RUN pip3 install pineboo==0.99.90.5
RUN echo "CREANDO USUARIO 'yeboyebo'"
RUN adduser --quiet --disabled-password --gecos '' yeboyebo 
RUN echo "yeboyebo:yeboyebo" | chpasswd 
RUN adduser yeboyebo sudo
RUN echo "COMPROBANDO EXISTENCIA USUARIO 'yeboyebo' y permisos"
RUN cat /etc/passwd | grep yeboyebo
USER yeboyebo
RUN whoami
RUN ls -la -R /src
