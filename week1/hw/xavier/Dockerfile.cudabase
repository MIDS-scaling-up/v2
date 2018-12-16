# FROM arm64v8/ubuntu:xenial-20180123
FROM arm64v8/ubuntu:xenial


# AUTHOR bmwshop@gmail.com
# This is the base container for the Jetson TX2 board with drivers (with cuda)

# base URL for NVIDIA libs
ARG URL=https://developer.download.nvidia.com/devzone/devcenter/mobile/jetpack_l4t/4.1.1/xddsn.im/JetPackL4T_4.1.1_b57

# Update packages, install some useful packages
RUN apt-get update && apt-get install -y apt-utils bzip2 curl sudo unp && apt-get clean && rm -rf /var/cache/apt
WORKDIR /tmp

# Install drivers first
# #RUN curl -sL http://developer.nvidia.com/embedded/dlc/l4t-jetson-tx2-driver-package-28-2 | tar xvfj -
## RUN chown root /etc/passwd /etc/sudoers /usr/lib/sudo/sudoers.so /etc/sudoers.d/README
## RUN /tmp/Linux_for_Tegra/apply_binaries.sh -r / && rm -fr /tmp/*

## Pull the rest of the jetpack libs for cuda/cudnn and install
# RUN curl $URL/cuda-repo-l4t-9-0-local_9.0.252-1_arm64.deb -so cuda-repo-l4t_arm64.deb
RUN curl $URL//cuda-repo-l4t-10-0-local-10.0.117_1.0-1_arm64.deb -so cuda-repo-l4t_arm64.deb

RUN curl $URL/libcudnn7_7.3.1.20-1+cuda10.0_arm64.deb -so /tmp/libcudnn_arm64.deb
RUN curl $URL/libcudnn7-dev_7.3.1.20-1+cuda10.0_arm64.deb -so /tmp/libcudnn-dev_arm64.deb

## Install libs: L4T, CUDA, cuDNN
RUN dpkg -i /tmp/cuda-repo-l4t_arm64.deb
RUN apt-key add /var/cuda-repo-10-0-local-10.0.117/7fa2af80.pub
RUN apt-get update && apt-get install -y cuda-toolkit-10.0
RUN dpkg -i /tmp/libcudnn_arm64.deb
RUN dpkg -i /tmp/libcudnn-dev_arm64.deb

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/tegra
ENV PATH=/usr/local/cuda-10.0/bin:$PATH
RUN apt-get -y autoremove && apt-get -y autoclean
RUN rm -rf /var/cache/apt
