# docker build -t hw6 -f Dockerfile . 
# docker images
# docker ps -a
# docker system prune
# 
# docker run -p 8888:8888 --rm -v /data:/data --name jupyter hw6

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
RUN apt-get update; apt-get install -y curl
RUN curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain=nightly -y
RUN echo rustc --version
# RUN pip install tokenizers
RUN git clone https://github.com/huggingface/transformers.git  && cd transformers && pip3 install . --no-dependencies  && cd .. && rm -rf transformers
#  RUN pip install tokenizers sentencepiece

WORKDIR /root

RUN git clone -b wk06hw https://github.com/MIDS-scaling-up/v2
WORKDIR /root/v2/week06/hw/data

#Configure container to support easier access
ARG TOKEN=12345678
RUN mkdir -p $HOME/.jupyter/
RUN if [ $TOKEN!=12345678 ]; then echo "c.NotebookApp.token='$TOKEN'" >> $HOME/.jupyter/jupyter_notebook_config.py; fi

EXPOSE 8888
CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root




