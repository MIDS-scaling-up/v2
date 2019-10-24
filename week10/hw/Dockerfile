# FROM eboraas/tensorflow:stable
FROM ubuntu:16.04

# credit where its due, for sure!
# MAINTAINER Ed Boraas <ed@boraas.ca>
MAINTAINER Dima Rekesh <bmwshop@gmail.com>  Esteban Arias <eariasn@us.ibm.com>


# docker build -t ubuntu1604py36
RUN apt-get update && \
  apt-get install -y software-properties-common vim && \
  add-apt-repository ppa:jonathonf/python-3.6


RUN apt-get update -y

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv && \
        apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade && \
        python3.6 -m pip install wheel


# credit where its due, for sure!
# MAINTAINER Ed Boraas <ed@boraas.ca>
 

# docker run -d -p 8888:8888 -p 6006:6006 --name openai -v /Users/drekesh/Downloads:/mnt/notebooks openai
# RUN apt-get update

# RUN apt-get -y install software-properties-common
# RUN add-apt-repository universe

# RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
RUN apt-get update 

RUN  apt-get -y install git
RUN apt-get install -y python-numpy python-dev cmake zlib1g-dev libjpeg-dev xvfb libav-tools xorg-dev python-opengl libboost-all-dev libsdl2-dev swig
# RUN apt-get -y install xvfb zlib1g python-opengl ffmpeg libsdl2-2.0-0 libboost-python1.62.0 libboost-thread1.62.0 libboost-filesystem1.62.0 libboost-system1.62.0 fluidsynth build-essential swig python-dev cmake zlib1g-dev libsdl2-dev libboost-all-dev wget unzip  

RUN apt-get install -y python-pip

# the latest version of gym is currently broken for whatever reason as of 01/31/2018
RUN pip --no-cache-dir install --upgrade 'gym==0.9.2'

RUN pip install git+https://github.com/jakevdp/JSAnimation.git 
RUN  add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN  apt-get install python3.6
# RUN dpkg --purge libsdl2-dev libboost-all-dev wget unzip && \
#      apt-get -y autoremove && \
#      dpkg --purge build-essential swig python-dev cmake zlib1g-dev && \
#      apt-get -y autoremove && \
#      apt-get clean && \
#      rm -r /var/lib/apt/lists/* /root/.cache/pip/

 

WORKDIR /

RUN git clone https://github.com/jakevdp/JSAnimation
WORKDIR /JSAnimation
RUN python setup.py install

RUN pip install --upgrade setuptools
COPY gym.ipynb /mnt/notebooks/

RUN pip install keras
RUN pip install tensorflow --upgrade
# Jupyter Notebook
RUN pip install jupyter
RUN pip install matplotlib
RUN pip3 uninstall pyglet -y
RUN pip3 install pyglet==1.3.2


EXPOSE 8888

# TensorBoard

EXPOSE 6006


WORKDIR /mnt/notebooks

 

RUN echo '#!/bin/bash' > /tmp/openai-gym.sh && \
    echo '/usr/bin/xvfb-run -s "-screen 0 1280x720x24" /usr/local/bin/jupyter-notebook --no-browser --ip=0.0.0.0 --allow-root --notebook-dir=/mnt/notebooks' >> /tmp/openai-gym.sh && \
    chmod +x /tmp/openai-gym.sh

CMD ["/tmp/openai-gym.sh"]
