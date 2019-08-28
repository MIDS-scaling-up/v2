FROM w251/tensorrt:dev-tx2-4.2.1_b97

RUN apt install -y cmake wget libblas-dev liblapack-dev libpython3-dev python3-pip python3-setuptools libnuma-dev
RUN wget https://nvidia.box.com/shared/static/06vlvedmqpqstu1dym49fo7aapgfyyu9.whl -O torch-1.2.0a0+8554416-cp36-cp36m-linux_aarch64.whl

RUN apt remove -y python3-numpy
RUN pip3 install numpy torch-1.2.0a0+8554416-cp36-cp36m-linux_aarch64.whl


RUN apt-get install -y libjpeg-dev zlib1g-dev
WORKDIR /tmp
RUN git clone -b v0.3.0 https://github.com/pytorch/vision torchvision
WORKDIR /tmp/torchvision
RUN python3 setup.py install

RUN rm -fr /tmp/torchvision

WORKDIR /
