FROM w251/cuda:dev-tx2-4.2_b158

WORKDIR /tmp

RUN apt update

ARG URL=http://169.44.201.108:7002/jetpacks/4.2

RUN curl $URL/libnvinfer5_5.0.6-1+cuda10.0_arm64.deb -so /tmp/libnvinfer5_5.0.6-1+cuda10.0_arm64.deb
RUN curl $URL/libnvinfer-dev_5.0.6-1+cuda10.0_arm64.deb -so /tmp/libnvinfer-dev_5.0.6-1+cuda10.0_arm64.deb
RUN curl $URL/libnvinfer-samples_5.0.6-1+cuda10.0_all.deb -so /tmp/libnvinfer-samples_5.0.6-1+cuda10.0_all.deb
RUN curl $URL/tensorrt_5.0.6.3-1+cuda10.0_arm64.deb -so /tmp/tensorrt_5.0.6.3-1+cuda10.0_arm64.deb

RUN curl $URL/python3-libnvinfer_5.0.6-1+cuda10.0_arm64.deb -so /tmp/python3-libnvinfer_5.0.6-1+cuda10.0_arm64.deb
RUN curl $URL/python3-libnvinfer-dev_5.0.6-1+cuda10.0_arm64.deb -so /tmp/python3-libnvinfer-dev_5.0.6-1+cuda10.0_arm64.deb


RUN apt install -y /tmp/*.deb
RUN apt install -y tensorrt python3-numpy

RUN rm /tmp/*.deb

# Clean up
RUN rm -fr /tmp/* /var/cache/apt/* && apt-get clean
