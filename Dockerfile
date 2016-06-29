FROM ubuntu:14.04
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential
RUN apt-get install -y python python-dev python-distribute python-pip

VOLUME /data

ADD ./ /pktables
RUN pip install -r /pktables/requirements.txt

WORKDIR /pktables
CMD python pktables.py
