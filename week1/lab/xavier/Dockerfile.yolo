# Original: FROM openhorizon/aarch64-tx2-cudabase
FROM cudabase:dev

# Install package dependencies
RUN apt-get update && apt-get install -y git pkg-config wget
RUN apt-get install -y libgtk2.0-dev pkg-config build-essential cmake libcanberra-gtk-module libcanberra-gtk3-module

# Install OpenCV
#RUN apt-get install -y libopencv-dev
# prep to install opencv
# Build tools:
RUN apt-get install -y build-essential cmake

# GUI (if you want to use GTK instead of Qt, replace 'qt5-default' with 'libgtkglext1-dev' and remove '-DWITH_QT=ON' option in CMake):
RUN apt-get update && apt-get install -y qt5-default libvtk6-dev

# Media I/O:
RUN apt-get install -y zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev

# Video I/O:
RUN apt-get install -y libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev

# Parallelism and linear algebra libraries:
RUN apt-get install -y libtbb-dev libeigen3-dev

# Python:
RUN apt-get install -y python-dev python-tk python-numpy python3-dev python3-tk python3-numpy

# Java:
RUN apt-get install -y ant default-jdk

# Documentation:
RUN apt-get install -y doxygen

# Install OpenCV
# RUN apt-get install -y libopencv-dev
ENV OPENCV_VERSION='3.4.2'

WORKDIR /tmp
RUN apt-get install -y unzip wget
RUN wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip
RUN unzip ${OPENCV_VERSION}.zip
RUN rm ${OPENCV_VERSION}.zip
RUN mv opencv-${OPENCV_VERSION} OpenCV
RUN cd OpenCV &&  mkdir build && cd build && cmake -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON -DENABLE_PRECOMPILED_HEADERS=OFF .. && make -j6 && make install
RUN ldconfig


# Install Darknet and Yolo
WORKDIR /
RUN git clone https://github.com/pjreddie/darknet.git
WORKDIR /darknet
# COPY Makefile /darknet/
RUN sed -i "s/^GPU=0/GPU=1/g" Makefile
RUN sed -i "s/^CUDNN=0/CUDNN=1/g" Makefile
RUN sed -i "s/^OPENCV=0/OPENCV=1/g" Makefile


# RUN ln -sf /usr/lib/aarch64-linux-gnu/tegra/libGL.so  /usr/lib/aarch64-linux-gnu/libGL.so
# ENV PATH $PATH:/usr/local/cuda-9.0/bin
#
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib/aarch64-linux-gnu
RUN make -j8 
RUN wget  https://pjreddie.com/media/files/yolov3.weights 
# this to get tiny-yolov3
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights


