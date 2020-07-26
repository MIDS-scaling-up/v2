FROM tensorflow/tensorflow:latest-gpu-py3
RUN apt-get -y update
# necessary to make add_user.sh work
RUN apt-get install -y --fix-missing sudo
# stuff opencv complains if they are not installed
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
RUN pip --no-cache-dir install \
opencv-python \
scikit-image
RUN pip install jupyter
RUN pip install keras
RUN pip install pandas
RUN pip install scikit-learn
#VOLUME /root
#WORKDIR /root
WORKDIR notebooks
RUN wget https://s3-eu-west-1.amazonaws.com/darraghdog1/train.csv.zip 
RUN wget https://s3-eu-west-1.amazonaws.com/darraghdog1/w251_lab04_1dcnn.ipynb
RUN wget http://nlp.stanford.edu/data/glove.6B.zip
RUN unzip glove.6B.zip
#RUN mkdir -p HW04
#RUN mkdir -p HW04/data
#RUN mkdir -p HW04/notebooks
EXPOSE 8888

#  CMD jupyter notebook --no-browser --ip=0.0.0.0 --NotebookApp.token= --allow-root
# CMD ["jupyter", "notebook", "--allow-root", "--debug", "--notebook-dir=notebooks", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root 


