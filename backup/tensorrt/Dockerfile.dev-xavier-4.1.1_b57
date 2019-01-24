FROM w251/cuda:dev-xavier-4.1.1_b57

WORKDIR /tmp


ARG URL=https://developer.download.nvidia.com/devzone/devcenter/mobile/jetpack_l4t/4.1.1/xddsn.im/JetPackL4T_4.1.1_b57

# GIE = TensorRT
# RUN curl $URL/libnvinfer4_4.1.3-1+cuda9.0_arm64.deb -so /tmp/libnvinfer4_4.1.3-1+cuda9.0_arm64.deb && dpkg -i /tmp/libnvinfer4_4.1.3-1+cuda9.0_arm64.deb
# RUN curl $URL/libnvinfer-dev_4.1.3-1+cuda9.0_arm64.deb -so /tmp/libnvinfer-dev_4.1.3-1+cuda9.0_arm64.deb && dpkg -i /tmp/libnvinfer-dev_4.1.3-1+cuda9.0_arm64.deb
# RUN curl $URL/libnvinfer-samples_4.1.3-1+cuda9.0_arm64.deb -so /tmp/libnvinfer-samples_4.1.3-1+cuda9.0_arm64.deb && dpkg -i /tmp/libnvinfer-samples_4.1.3-1+cuda9.0_arm64.deb
# RUN curl $URL/tensorrt_4.0.2.0-1+cuda9.0_arm64.deb -so /tmp/tensorrt_4.0.2.0-1+cuda9.0_arm64.deb && dpkg -i /tmp/tensorrt_4.0.2.0-1+cuda9.0_arm64.deb
# RUN curl $URL/libgie-dev_4.1.3-1+cuda9.0_arm64.deb -so /tmp/libgie-dev_4.1.3-1+cuda9.0_arm64.deb && dpkg -i /tmp/libgie-dev_4.1.3-1+cuda9.0_arm64.deb


RUN curl $URL/libnvinfer5_5.0.3-1+cuda10.0_arm64.deb -so /tmp/libnvinfer5_5.0.3-1+cuda10.0_arm64.deb && dpkg -i /tmp/libnvinfer5_5.0.3-1+cuda10.0_arm64.deb
RUN curl $URL/libnvinfer-dev_5.0.3-1+cuda10.0_arm64.deb -so /tmp/libnvinfer-dev_5.0.3-1+cuda10.0_arm64.deb && dpkg -i /tmp/libnvinfer-dev_5.0.3-1+cuda10.0_arm64.deb
RUN curl $URL/libnvinfer-samples_5.0.3-1+cuda10.0_all.deb -so /tmp/libnvinfer-samples_5.0.3-1+cuda10.0_all.deb && dpkg -i /tmp/libnvinfer-samples_5.0.3-1+cuda10.0_all.deb
RUN curl $URL/tensorrt_5.0.3.2-1+cuda10.0_arm64.deb -so /tmp/tensorrt_5.0.3.2-1+cuda10.0_arm64.deb && dpkg -i /tmp/tensorrt_5.0.3.2-1+cuda10.0_arm64.deb
RUN curl $URL/libgie-dev_5.0.3-1+cuda10.0_all.deb -so /tmp/libgie-dev_5.0.3-1+cuda10.0_all.deb && dpkg -i /tmp/libgie-dev_5.0.3-1+cuda10.0_all.deb

RUN apt-get update && apt-get install -y tensorrt



# Clean up
RUN rm -fr /tmp/* /var/cache/apt/* && apt-get clean
