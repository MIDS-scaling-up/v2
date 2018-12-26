FROM tensorrt

# to run, do xhost + on the host then
# docker run --privileged -v /dev:/dev -e DISPLAY=$DISPLAY -v /tmp:/tmp --net=host --ipc=host --rm -ti openhorizon/dustyinference bash -c "cd /jetson-inference/build/aarch64/bin && ./imagenet-camera"

WORKDIR /

RUN apt-get update || true
RUN apt-get -y install git cmake wget gstreamer1.0-plugins-good 
RUN git clone https://github.com/dusty-nv/jetson-inference

# switch to using /dev/video0 instead of jetsons own camera -1
#RUN sed -i "s/#define DEFAULT_CAMERA -1/#define DEFAULT_CAMERA 0/g" /jetson-inference/imagenet-camera/imagenet-camera.cpp

WORKDIR /jetson-inference
RUN mkdir build
WORKDIR /jetson-inference/build
RUN cmake ../ 
RUN make -j4
WORKDIR /jetson-inference
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/tegra-egl/
#COPY bashrc /root/.bashrc
RUN echo "export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:/usr/lib/aarch64-linux-gnu/tegra:/usr/lib/aarch64-linux-gnu/tegra-egl/" >> /root/.bashrc
RUN apt-get clean
