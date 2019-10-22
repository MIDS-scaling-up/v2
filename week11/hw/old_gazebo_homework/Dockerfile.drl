FROM w251/cuda:dev-tx2-4.2_b158

# validated on 3/24/2019
# to run a quick test demo without building the container:
# allow x clients to connect, so type this from any terminal logged into your tx2:
# xhost + 
# then
# docker run --rm -v /tmp:/tmp -v /dev:/dev --ipc=host --net=host --privileged -e DISPLAY=$DISPLAY w251/drl:tx2-3.3_b39
#  sh -c "cd /jetson-reinforcement/build/aarch64/bin && ./gazebo-arm.sh"
# It will take some time to start

# to start an interactive shell:
# docker run --rm -v /tmp:/tmp -v /dev:/dev --ipc=host --net=host --privileged -e DISPLAY=$DISPLAY -ti w251/drl:tx2-3.3_b39 bash

# to build this container locally
# docker build -t drl -f Dockerfile.drl .
# Note that it will take several hours..

RUN apt update
RUN apt install -y git cmake

WORKDIR /
RUN git clone http://github.com/dusty-nv/jetson-reinforcement
WORKDIR /jetson-reinforcement
RUN git submodule update --init
# RUN mkdir build
# WORKDIR /jetson-reinforcement/build

RUN sed -i -e 's/apt-get install -y/apt-get install/g' CMakePreBuild.sh && sed -i -e 's/apt-get install/apt-get install -y/g' CMakePreBuild.sh
RUN sed -i '32,39d' CMakePreBuild.sh && sed -i '32i sudo apt-get install -y gazebo7 libgazebo7-dev' CMakePreBuild.sh
RUN sed -i '68,75d' CMakePreBuild.sh && sed -i '68i sudo apt-get install -y ipython ipython-notebook; sudo pip install jupyter' CMakePreBuild.sh

# Build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt install -y tzdata libboost-all-dev qt4-default
RUN mkdir build
WORKDIR build
RUN cmake ../
RUN make -j6

# ENV DEBIAN_FRONTEND=noninteractive
# locale madness
RUN apt install -y locales locales-all gnome-terminal
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
