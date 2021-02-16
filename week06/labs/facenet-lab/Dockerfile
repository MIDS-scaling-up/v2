# to build:
# docker build -t facenet -f Dockerfile .
# to rim"
# docker run --rm --runtime nvidia -p 8888:8888 -ti facenet
# jupyter will start automatically
# FROM nvcr.io/nvidia/l4t-ml:r32.4.4-py3

# we built our own version using the latest from https://github.com/dusty-nv/jetson-containers
# as it includes opencv for instance
FROM w251/l4t-ml:r32.4.4-py3

RUN pip3 install facenet-pytorch

RUN git clone https://github.com/timesler/facenet-pytorch.git facenet_pytorch
ADD facedetect.ipynb /facenet_pytorch/examples/
ADD facedetect_cv2.ipynb /facenet_pytorch/examples/

# fix the latest jupyter password issues
RUN rm /root/.jupyter/*
