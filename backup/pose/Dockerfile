# docker run --rm --privileged --runtime=nvidia -p 8888:8888 bash
# followed by jupyter notebook password
# then jupyter notebook --ip=0.0.0.0 --allow-root

ARG BASE_IMAGE=nvcr.io/nvidia/l4t-ml:r32.4.3-py3

FROM ${BASE_IMAGE} 

WORKDIR /
RUN apt update

RUN git clone https://github.com/NVIDIA-AI-IOT/jetcam
WORKDIR /jetcam
RUN python3 setup.py install

WORKDIR /
RUN git clone https://github.com/NVIDIA-AI-IOT/torch2trt
WORKDIR /torch2trt
RUN python3 setup.py install --plugins

WORKDIR /
RUN pip3 install tqdm cython pycocotools
RUN apt install -y python3-matplotlib
RUN git clone https://github.com/NVIDIA-AI-IOT/trt_pose
WORKDIR /trt_pose
RUN python3 setup.py install

RUN apt install -y gnupg2
COPY nvidia-l4t-apt-source.list /etc/apt/sources.list.d/
COPY trusted-keys /tmp/
RUN apt-key add /tmp/trusted-keys
RUN apt update
RUN apt install -y nvidia-opencv

# these come from https://github.com/NVIDIA-AI-IOT/trt_pose
COPY densenet121_baseline_att_256x256_B_epoch_160.pth tasks/human_pose/
COPY resnet18_baseline_att_224x224_A_epoch_249.pth tasks/human_pose/
