# Original: FROM openhorizon/aarch64-tx2-cudabase
FROM cudabase

# Install package dependencies
RUN apt-get update && apt-get install -y git pkg-config wget
RUN apt-get install -y libgtk2.0-dev pkg-config build-essential cmake libcanberra-gtk-module libcanberra-gtk3-module

# Install OpenCV
 RUN apt-get install -y libopencv-dev

# Install Darknet and Yolo
WORKDIR /
RUN git clone https://github.com/pjreddie/darknet.git
WORKDIR /darknet
COPY Makefile /darknet/
ENV PATH $PATH:/usr/local/cuda-9.0/bin
RUN make -j4 
RUN wget  https://pjreddie.com/media/files/yolov3.weights 
# this to get tiny-yolov3
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights


