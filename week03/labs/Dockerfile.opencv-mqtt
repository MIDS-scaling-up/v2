FROM ubuntu

# build this: e.g docker build -t motion -f Dockerfile.opencv-mqtt
# to run this container, do:
# on the host:
# make sure you're in the X environment
# xhost + 
# docker run --rm --privileged -e DISPLAY -v /tmp:/tmp -ti motion bash

RUN apt update

ENV DEBIAN_FRONTEND=noninteractive

RUN apt install -y python-opencv python-pip vim-tiny mosquitto-clients libopencv-dev
RUN pip install paho-mqtt

WORKDIR /
