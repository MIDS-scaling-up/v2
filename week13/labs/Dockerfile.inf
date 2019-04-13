FROM w251/cuda:tx2-3.3_b39

# to run this in interactive mode, try
# docker run --rm --privileged -v /tmp:/tmp -v /var:/var -v /home/nvidia/models:/models --net=host --ipc=host --env DISPLAY=$DISPLAY -ti w251/inf:tx2-3.3_b39 bash
# Try the frame classification demo:
# ./imagenet-camera
# Try the object detection demo:
# ./detectnet-camera
# Try the segmentation demo:
# ./segnet-camera

RUN apt update
RUN apt install -y git cmake wget gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-base
WORKDIR /tmp
RUN rm *.deb
ARG URL=https://developer.download.nvidia.com/devzone/devcenter/mobile/jetpack_l4t/3.3/lw.xd42/JetPackL4T_33_b39/

RUN wget $URL/libopencv_3.3.1_t186_arm64.deb
RUN wget $URL/libopencv-dev_3.3.1_t186_arm64.deb
RUN wget $URL/libopencv-python_3.3.1_t186_arm64.deb
RUN wget $URL/libopencv-samples_3.3.1_t186_arm64.deb

RUN wget $URL/libnvinfer4_4.1.3-1+cuda9.0_arm64.deb
RUN wget $URL/libnvinfer-dev_4.1.3-1+cuda9.0_arm64.deb
RUN wget $URL/libnvinfer-samples_4.1.3-1+cuda9.0_arm64.deb

RUN apt install -y /tmp/*.deb
RUN rm *.deb

WORKDIR /
RUN git clone http://github.com/dusty-nv/jetson-inference
WORKDIR /jetson-inference
RUN git submodule update --init
RUN mkdir build
WORKDIR /jetson-inference/build

# Build

RUN cmake ../
RUN make -j6

RUN make install

WORKDIR /jetson-inference/build/aarch64/bin
