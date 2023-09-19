FROM python:3.10.5-buster

MAINTAINER Javier Cortés <javier@yeboyebo.es>

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y apt-utils build-essential vim tzdata libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev freetds-dev libgl1 libegl1 libxkbcommon-x11-0 libjpeg-dev libdbus-1-3

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /pineboo/
RUN mkdir /src/
RUN mkdir /src/app/
RUN mkdir /src/app/logs
WORKDIR /src/
ADD requirements.txt /src/
RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN pip3 install --upgrade setuptools==57.5.0
RUN pip3 install -r requirements.txt --use-deprecated=legacy-resolver
RUN pip3 install pineboo==0.99.76.2
RUN adduser --quiet --disabled-password --gecos '' yeboyebo && echo "yeboyebo:yeboyebo" | chpasswd && adduser yeboyebo sudo
