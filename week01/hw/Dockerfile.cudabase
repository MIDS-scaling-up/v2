FROM arm64v8/ubuntu:bionic


# AUTHOR bmwshop@gmail.com
# This is the base container for the Jetson TX2 board with drivers (with cuda)


ARG URL=http://169.44.201.108:7002/jetpacks/4.2

# Update packages, install some useful packages
RUN apt-get update && apt-get install -y gnupg2 apt-utils bzip2 curl sudo unp && apt-get clean && rm -rf /var/cache/apt
WORKDIR /tmp

RUN curl $URL/cuda-repo-l4t-10-0-local-10.0.166_1.0-1_arm64.deb -so cuda-repo-l4t_arm64.deb
RUN curl $URL/libcudnn7_7.3.1.28-1+cuda10.0_arm64.deb -so libcudnn_arm64.deb
RUN curl $URL/libcudnn7-dev_7.3.1.28-1+cuda10.0_arm64.deb -so libcudnn-dev_arm64.deb


## Install libs: L4T, CUDA, cuDNN
RUN dpkg -i /tmp/cuda-repo-l4t_arm64.deb
RUN apt-key add /var/cuda-repo-10-0-local-10.0.166/7fa2af80.pub
RUN apt-get update && apt-get install -y cuda-toolkit-10.0
RUN dpkg -i /tmp/libcudnn_arm64.deb
RUN dpkg -i /tmp/libcudnn-dev_arm64.deb

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/tegra
ENV PATH=/usr/local/cuda-10.0/bin:$PATH
RUN apt-get -y autoremove && apt-get -y autoclean
RUN rm -rf /var/cache/apt
RUN rm -f /tmp/*.deb
