FROM w251/cuda:tx2-3.3_b39
#AUTHOR chenbryanchen@gmail.com

WORKDIR /tmp

#ARG URL=https://developer.download.nvidia.com/devzone/devcenter/mobile/jetpack_l4t/3.2.1/m8u2ki/JetPackL4T_321_b23/
ARG URL=https://developer.download.nvidia.com/devzone/devcenter/mobile/jetpack_l4t/3.3/lw.xd42/JetPackL4T_33_b39/

# GIE = TensorRT
#RUN curl $URL/nv-tensorrt-repo-ubuntu1604-ga-cuda9.0-trt3.0.4-20180208_1-1_arm64.deb -so /tmp/nv-tensorrt-repo-ubuntu1604-ga-cuda9.0-trt3.0.4-20180208_1-1_arm64.deb
#RUN dpkg -i /tmp/nv-tensorrt-repo-ubuntu1604-ga-cuda9.0-trt3.0.4-20180208_1-1_arm64.deb
RUN curl $URL/libnvinfer4_4.1.3-1+cuda9.0_arm64.deb -so /tmp/libnvinfer4_4.1.3-1+cuda9.0_arm64.deb && dpkg -i /tmp/libnvinfer4_4.1.3-1+cuda9.0_arm64.deb
RUN curl $URL/libnvinfer-dev_4.1.3-1+cuda9.0_arm64.deb -so /tmp/libnvinfer-dev_4.1.3-1+cuda9.0_arm64.deb && dpkg -i /tmp/libnvinfer-dev_4.1.3-1+cuda9.0_arm64.deb
RUN curl $URL/libnvinfer-samples_4.1.3-1+cuda9.0_arm64.deb -so /tmp/libnvinfer-samples_4.1.3-1+cuda9.0_arm64.deb && dpkg -i /tmp/libnvinfer-samples_4.1.3-1+cuda9.0_arm64.deb
RUN curl $URL/tensorrt_4.0.2.0-1+cuda9.0_arm64.deb -so /tmp/tensorrt_4.0.2.0-1+cuda9.0_arm64.deb && dpkg -i /tmp/tensorrt_4.0.2.0-1+cuda9.0_arm64.deb
RUN curl $URL/libgie-dev_4.1.3-1+cuda9.0_arm64.deb -so /tmp/libgie-dev_4.1.3-1+cuda9.0_arm64.deb && dpkg -i /tmp/libgie-dev_4.1.3-1+cuda9.0_arm64.deb

RUN apt-get update && apt-get install -y tensorrt

# TODO: figure out the source of these libs, they're on the fs prepped by jetpack but not in downloadable sample root fs
#RUN rm /usr/lib/aarch64-linux-gnu/libcuda.so* /usr/lib/aarch64-linux-gnu/tegra/libcuda.so*
#RUN ln -s /usr/lib/aarch64-linux-gnu/tegra/libcuda.so.1.1 /usr/lib/aarch64-linux-gnu/tegra/libcuda.so
#RUN curl -sL http://1dd40.http.tor01.cdn.softlayer.net/nvidia-media/JetPack-L4T-3.2-linux-x64_b157-rootfs-extracts.tar.gz | tar xfz - -C /

# Dev
RUN apt-get install -y vim

# Clean up
RUN rm -fr /tmp/* /var/cache/apt/* && apt-get clean
