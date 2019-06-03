FROM tensorflow/tensorflow:latest-py3
RUN apt-get -y update
RUN apt-get install -y --fix-missing sudo
RUN apt-get install -y --fix-missing \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgtk2.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    wget
RUN apt-get clean && rm -rf /tmp/* /var/tmp/*
RUN pip install jupyter
RUN pip install keras
RUN pip install pandas
RUN pip install scikit-learn
#VOLUME /root
#WORKDIR /root
RUN mkdir -p notebooks
WORKDIR notebooks
RUN wget https://s3-eu-west-1.amazonaws.com/darraghdog1/train.csv.zip
RUN wget https://github.com/MIDS-scaling-up/v2/blob/darragh_hw04/week04/hw/w251_homework04.ipynb
#RUN wget https://s3-eu-west-1.amazonaws.com/darraghdog1/w251_homework04.ipynb
#RUN mkdir -p HW04
#RUN mkdir -p HW04/data
#RUN mkdir -p HW04/notebooks
EXPOSE 8888

# Jupyter
CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root


