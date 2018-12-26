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
RUN curl -sL $URL/Jetson_Linux_R31.1.0_aarch64.tbz2 | tar xvfj -
RUN chown root /etc/passwd /etc/sudoers /usr/lib/sudo/sudoers.so /etc/sudoers.d/README

RUN sed -i "s/LDK_NV_TEGRA_DIR}\/config.tbz2/LDK_NV_TEGRA_DIR}\/config.tbz2 --exclude=etc\/hosts --exclude=etc\/hostname/g"  /tmp/Linux_for_Tegra/apply_binaries.sh

# #RUN curl -sL http://developer.nvidia.com/embedded/dlc/l4t-jetson-tx2-driver-package-28-2 | tar xvfj -
## RUN chown root /etc/passwd /etc/sudoers /usr/lib/sudo/sudoers.so /etc/sudoers.d/README
RUN /tmp/Linux_for_Tegra/apply_binaries.sh -r / && rm -fr /tmp/*

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

###
# RUN curl $URL/libopencv-dev_3.3.1_arm64.deb -so /tmp/libopencv-dev_arm64.deb
# RUN dpkg -i /tmp/libopencv-dev_arm64.deb
#### libglvnd
WORKDIR /tmp
RUN apt-get update
# RUN apt-get install -y libxext-dev libx11-dev x11proto-gl-dev git build-essential automake autogen autoconf libtool python
RUN apt-get install -y libxext-dev libx11-dev x11proto-gl-dev git automake autoconf libtool python pkg-config


RUN git clone https://github.com/NVIDIA/libglvnd.git
WORKDIR /tmp/libglvnd

RUN ./autogen.sh
RUN ./configure 
RUN make -j 6 
RUN make install
RUN rm -fr /tmp/libglvnd

WORKDIR /

# the required softlinks
RUN rm -f /usr/lib/aarch64-linux-gnu/libGL.so
RUN ln -s /usr/lib/aarch64-linux-gnu/libGLU.so /usr/lib/aarch64-linux-gnu/libGL.so
RUN ln -s /usr/lib/aarch64-linux-gnu/libcuda.so /usr/lib/aarch64-linux-gnu/libcuda.so.1
RUN ln -s /usr/lib/aarch64-linux-gnu/tegra/libnvidia-ptxjitcompiler.so.31.1.0 /usr/lib/aarch64-linux-gnu/tegra/libnvidia-ptxjitcompiler.so.1

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/tegra
ENV PATH=/usr/local/cuda-10.0/bin:$PATH
RUN apt-get -y autoremove && apt-get -y autoclean
RUN rm -rf /var/cache/apt
