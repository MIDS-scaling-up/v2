# Original: FROM openhorizon/aarch64-tx2-cudabase
FROM cudabase

RUN apt-get update && apt-get install -y git pkg-config wget
RUN apt-get install -y build-essential cmake
RUN apt-get install -y libgtk2.0-dev && apt-get install -y pkg-config
# RUN apt-get install -y libgstreamer-plugins-base1.0-0 libgstreamer1.0 libgstreamer-plugins-good1.0-0 libgstreamer-plugins-good1.0-dev

RUN rm -R /usr/lib/aarch64-linux-gnu/gstreamer-1.0/
COPY gstreamer-1.0 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/

# RUN apt-get install -y libopencv-dev

WORKDIR /

RUN git clone https://github.com/AlexanderRobles21/OpenCVTX2
WORKDIR /OpenCVTX2
RUN sh buildOpenCV.sh
WORKDIR /root/opencv/build
RUN make 
# WORKDIR /root/opencv/build
RUN sudo make install

WORKDIR /
RUN git clone https://github.com/pjreddie/darknet.git
WORKDIR /darknet
COPY Makefile /darknet/
ENV PATH $PATH:/usr/local/cuda-9.0/bin
RUN make -j4 

RUN wget  https://pjreddie.com/media/files/yolov3.weights 
# this to get tiny-yolov3
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights

# use this terminal command to create a container that immediately runs yolo with webcam. container is deleted afterwards
# docker run -e DISPLAY=$DISPLAY --rm  --privileged -v /tmp:/tmp yolo ./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights -c 1


# or run with tiny-yolo
# docker run -e DISPLAY=$DISPLAY --rm  --privileged -v /tmp:/tmp yolo ./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights -c 1

