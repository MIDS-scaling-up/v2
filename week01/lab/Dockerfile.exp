# Original: FROM openhorizon/aarch64-tx2-cudabase

# this is an experimental docker file that should eventually support TX2's onboard camera
FROM cudabase

# Install package dependencies
RUN apt-get update && apt-get install -y git pkg-config wget
RUN apt-get install -y libgtk2.0-dev pkg-config build-essential cmake libcanberra-gtk-module libcanberra-gtk3-module
# RUN apt-get install -y libgstreamer-plugins-base1.0-0 libgstreamer1.0 libgstreamer-plugins-good1.0-0 libgstreamer-plugins-good1.0-dev

#Install OpenCV. The first commented line is an older version
# RUN apt-get install -y libopencv-dev
WORKDIR /
RUN git clone https://github.com/AlexanderRobles21/OpenCVTX2
WORKDIR /OpenCVTX2
RUN sed -i '72i -D WITH_LIBV4L=ON \\' buildOpenCV.sh
RUN sh buildOpenCV.sh
WORKDIR /root/opencv/build
RUN make 
RUN sudo make install

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
