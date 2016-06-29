#!/bin/bash

set -o allexport
source ./env.local
set +o allexport

echo $PACKETKEY
echo $PROJECTID
echo $RULESFILE
python pktables.py
