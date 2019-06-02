FROM w251/nvcaffe:tx2-4.2_b158
# AUTHOR chenbryanchen@gmail.com

WORKDIR /
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install --upgrade pip
RUN apt-get install --no-install-recommends -y git graphviz python-dev python-flask python-flaskext.wtf python-gevent python-h5py python-numpy python-pil python-protobuf python-scipy python-tk

# RUN apt-get install -y python-matplotlib=1.5
RUN apt install -y libfreetype6-dev
ENV CAFFE_ROOT /caffe
ENV DIGITS_ROOT /digits
RUN git clone https://github.com/NVIDIA/DIGITS.git 

RUN sed -i '4d' /DIGITS/requirements.txt
RUN pip install -r /DIGITS/requirements.txt
RUN pip install -e /DIGITS
CMD /DIGITS/digits-devserver -p 5001
