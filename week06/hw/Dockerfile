# docker build -t hw6 -f Dockerfile . 
FROM nvcr.io/nvidia/l4t-ml:r32.4.3-py3


RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip
# Install dependencies
RUN pip install jupyter
RUN pip install nltk
RUN pip install setuptools-rust
RUN pip install regex 
RUN pip install tqdm
RUN pip install requests
RUN pip install filelock
RUN pip install packaging
RUN pip install sacremoses
RUN git clone https://github.com/huggingface/transformers.git  && \
    cd transformers && pip3 install . && \
    cd .. && rm -rf transformers
#  RUN apt-get update; apt-get install curl
#  RUN curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain=nightly -y
#  RUN pip install tokenizers filelock requests tqdm regex 
#  sacremoses  packaging
#  RUN git clone https://github.com/huggingface/transformers.git  && \
    cd transformers && pip3 install . --no-dependencies && cd .. && rm -rf transformers


WORKDIR /root

RUN git clone https://github.com/MIDS-scaling-up/v2
WORKDIR /root/v2/week06/hw/data

EXPOSE 8888
CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root
