# build like this:
# docker build -t lab09 .
# run like this:
# docker run --rm --gpus all -v /data2:/data -p 8888:8888 --ipc=host -ti lab09 bash
# or, if you don't want to build it,
# docker run --rm --gpus all -v /data2:/data -p 8888:8888 --ipc=host -ti w251/lab09 bash

FROM nvcr.io/nvidia/pytorch:20.09-py3 

RUN pip install ipywidgets
RUN pip install transformers
# install node
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt install -y nodejs

RUN pip install tqdm -U

RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager

CMD jupyter lab --ip=0.0.0.0 --allow-root
