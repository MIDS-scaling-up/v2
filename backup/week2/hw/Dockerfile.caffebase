# FROM openhorizon/aarch64-tx2-cudabase:JetPack3.2-RC
FROM cudabase

#AUTHOR chenbryanchen@gmail.com

ENV ARCH=aarch64

WORKDIR /

# Install opencv dev package libraries
RUN apt-get update && apt-get install -y libopencv-dev

# Install dependencies
RUN apt-get install -y --no-install-recommends build-essential cmake git gfortran libatlas-base-dev libboost-filesystem-dev libboost-python-dev libboost-system-dev libboost-thread-dev libgflags-dev libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libsnappy-dev python-all-dev python-dev python-h5py python-matplotlib python-numpy python-opencv python-pil python-pip python-scipy python-skimage python-sklearn python-setuptools autoconf automake libtool 

# Install newer protobuf
RUN mkdir /protobuf
WORKDIR /protobuf
RUN git clone -b '3.6.x' https://github.com/google/protobuf.git . && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local/protobuf && \
    make "-j$(nproc)" install
RUN cp -r /usr/local/protobuf/* /usr/local
WORKDIR /
RUN rm -fr /protobuf

RUN pip install --upgrade pip 
RUN pip install protobuf==3.6.0
RUN git clone http://github.com/NVIDIA/caffe -b 'caffe-0.15'

# patch caffe for aarch64
COPY mutex.patch /tmp/mutex.patch
RUN patch /caffe/3rdparty/cub/host/mutex.cuh /tmp/mutex.patch

# Install Caffe
WORKDIR /caffe/python
RUN for req in $(cat requirements.txt); do pip install $req; done
WORKDIR /caffe
RUN mkdir build
WORKDIR /caffe/build
RUN cmake ../ -DCUDA_ARCH_NAME="Manual" -DCUDA_ARCH_BIN="52 60" -DCUDA_ARCH_PTX="60"

# Fix cmake_cxx_flags 
WORKDIR /caffe/src/caffe
RUN sed -i '1i set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")' CMakeLists.txt
WORKDIR /caffe/tools
RUN sed -i '1i set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")' CMakeLists.txt
WORKDIR /caffe/examples
RUN sed -i '1i set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")' CMakeLists.txt
WORKDIR /caffe/python
RUN sed -i '1i set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")' CMakeLists.txt

WORKDIR /caffe/build
RUN make --jobs=6
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/tegra
RUN make pycaffe -j5
RUN make test -j5

# Clean up
RUN apt-get -y autoremove && apt-get -y clean
