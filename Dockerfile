FROM python:3-alpine

VOLUME /data

ADD ./ /pktables
RUN pip install -r /pktables/requirements.txt

WORKDIR /pktables
CMD python pktables.py
