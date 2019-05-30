FROM w251/tensorflow:dev-tx2-4.2_b158-py3

# This is a container for Keras and Jupyter
# docker run --name keras --privileged -p 8888:8888 -d w251/keras:dev-tx2-4.2_b158-py3 


RUN apt update
RUN apt install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgtk2.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    wget

RUN pip3 install jupyter
RUN pip3 install pandas

ENV DEBIAN_FRONTEND=noninteractive
RUN apt install -y python3-sklearn
RUN pip3 install keras

WORKDIR /
RUN mkdir -p notebooks
WORKDIR /notebooks

EXPOSE 8888

# Jupyter
CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root

