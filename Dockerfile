FROM python:3.6.10-buster

MAINTAINER Javier Cortés <javier@yeboyebo.es>

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y apt-utils build-essential python3-pip vim python3-pyqt5 tzdata libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /pineboo/
RUN mkdir /src/
RUN mkdir /src/app/
RUN mkdir /src/app/logs
WORKDIR /src/
ADD requirements.txt /src/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install pineboo==0.75
RUN adduser --quiet --disabled-password --gecos '' yeboyebo && echo "yeboyebo:yeboyebo" | chpasswd && adduser yeboyebo sudo
