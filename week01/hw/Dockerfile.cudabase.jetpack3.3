#FROM aarch64/ubuntu
# FROM arm64v8/ubuntu:xenial-20180123
FROM arm64v8/ubuntu:xenial

#AUTHOR chenbryanchen@gmail.com
# This is the base container for the Jetson TX2 board with drivers (with cuda) for the Scaling Up class (original Dockerfile at https://github.com/open-horizon/cogwerx-jetson-tx2/blob/master/Dockerfile.cudabase)

# base URL for NVIDIA libs
ARG URL=https://developer.download.nvidia.com/devzone/devcenter/mobile/jetpack_l4t/3.3/lw.xd42/JetPackL4T_33_b39/

# Update packages, install some useful packages
RUN apt-get update && apt-get install -y apt-utils bzip2 curl sudo unp && apt-get clean && rm -rf /var/cache/apt
WORKDIR /tmp

# Install drivers first
#RUN curl -sL https://developer.nvidia.com/embedded/dlc/tx2-driver-package-r2821 | tar jxvf -
RUN curl -sL http://developer.nvidia.com/embedded/dlc/l4t-jetson-tx2-driver-package-28-2 | tar xvfj -
RUN chown root /etc/passwd /etc/sudoers /usr/lib/sudo/sudoers.so /etc/sudoers.d/README
RUN /tmp/Linux_for_Tegra/apply_binaries.sh -r / && rm -fr /tmp/*

## Pull the rest of the jetpack libs for cuda/cudnn and install
RUN curl $URL/cuda-repo-l4t-9-0-local_9.0.252-1_arm64.deb -so cuda-repo-l4t_arm64.deb
RUN curl $URL/libcudnn7_7.1.5.14-1+cuda9.0_arm64.deb -so /tmp/libcudnn_arm64.deb
RUN curl $URL/libcudnn7-dev_7.1.5.14-1+cuda9.0_arm64.deb -so /tmp/libcudnn-dev_arm64.deb

## Install libs: L4T, CUDA, cuDNN
RUN dpkg -i /tmp/cuda-repo-l4t_arm64.deb
RUN apt-key add /var/cuda-repo-9-0-local/7fa2af80.pub
# ----------------------------^^updated^^---------------------------------------
RUN apt-get update && apt-get install -y cuda-toolkit-9.0
RUN dpkg -i /tmp/libcudnn_arm64.deb
RUN dpkg -i /tmp/libcudnn-dev_arm64.deb
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/tegra


## Re-link libs in /usr/lib/<arch>/tegra
RUN ln -s /usr/lib/aarch64-linux-gnu/tegra/libnvidia-ptxjitcompiler.so.28.2.0 /usr/lib/aarch64-linux-gnu/tegra/libnvidia-ptxjitcompiler.so
RUN ln -s /usr/lib/aarch64-linux-gnu/tegra/libnvidia-ptxjitcompiler.so.28.2.0 /usr/lib/aarch64-linux-gnu/tegra/libnvidia-ptxjitcompiler.so.1
RUN ln -sf /usr/lib/aarch64-linux-gnu/tegra/libGL.so /usr/lib/aarch64-linux-gnu/libGL.so
# D.R. -- need to do this for some strange reason (for jetson tx2)
RUN ln -s /usr/lib/aarch64-linux-gnu/libcuda.so /usr/lib/aarch64-linux-gnu/libcuda.so.1

## Clean up (don't remove cuda libs... used by child containers)
RUN apt-get -y autoremove && apt-get -y autoclean
RUN rm -rf /var/cache/apt
