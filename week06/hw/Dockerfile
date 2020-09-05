# docker build -t hw6 -f Dockerfile . 
# docker images
# docker ps -a
# docker system prune
# 
# docker run -p 8888:8888 --rm -v /data:/data --name jupyter hw6
# docker build -t hw6 -f Dockerfile . 
FROM nvcr.io/nvidia/l4t-ml:r32.4.3-py3


RUN rm /usr/bin/python
# RUN rm /usr/bin/pip
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

RUN apt update
# sentecepiece
RUN apt-get install -y cmake build-essential pkg-config libgoogle-perftools-dev
RUN git clone -b v0.1.85 https://github.com/google/sentencepiece/ sentencepiece-0.1.85
RUN cd sentencepiece-0.1.85 && mkdir build && cd build && cmake .. && make -j $(nproc) && make install && ldconfig -v && \
    cd ../python && python3 setup.py bdist_wheel && cd dist && pip3 install sentencepiece-0.1.85-cp36-cp36m-linux_aarch64.whl --verbose

# rust
RUN apt install -y curl

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > r.sh
RUN chmod 777 ./r.sh && ./r.sh -y
ENV HOME=/root
ENV PATH=${HOME}/.cargo/bin:${PATH} 
RUN pip3 install setuptools_rust
RUN PATH=${HOME}/.cargo/bin:${PATH} 
RUN PYTHONPATH=${HOME}/.cargo/bin:${PYTHONPATH} 

RUN echo $PATH
RUN rustc --version

#### tokenizers
RUN pip3 install tokenizers


#############################
RUN git clone https://github.com/huggingface/transformers.git  && \
    cd transformers && pip3 install . && \
    cd .. && rm -rf transformers

WORKDIR /root

RUN git clone -b wk06hw https://github.com/MIDS-scaling-up/v2
WORKDIR /root/v2/week06/hw/data


#Configure container to support easier access
ARG TOKEN=12345678
RUN mkdir -p $HOME/.jupyter/
RUN if [ $TOKEN!=12345678 ]; then echo "c.NotebookApp.token='$TOKEN'" >> $HOME/.jupyter/jupyter_notebook_config.py; fi

EXPOSE 8888
CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root




