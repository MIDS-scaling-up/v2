# This builds the tensorrt lab file docker file 
# docker build -t tensorrtlab05 -f Dockerfile.tensorrtlab05 .
# docker run --privileged --rm -p 8888:8888 -d tensorrtlab05

FROM w251/keras:dev-tx2-4.2_b158-py3

RUN apt update && apt install python3-matplotlib python3-pil wget -y


###### install the c++ version of protobuf ####
RUN pip3 uninstall -y protobuf
RUN pip3 install cython

RUN mkdir /protobuf
WORKDIR /protobuf
RUN git clone -b '3.6.x' https://github.com/google/protobuf.git . && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local 

RUN make -j6 && make install
RUN ldconfig

WORKDIR /protobuf/python
RUN python3 setup.py build --cpp_implementation
RUN python3 setup.py install --cpp_implementation
RUN rm -fr /protobuf
WORKDIR /notebooks
###########
RUN git clone --recursive https://github.com/NVIDIA-Jetson/tf_trt_models.git
WORKDIR tf_trt_models
RUN ./install.sh python3

 
