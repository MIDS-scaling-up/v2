FROM w251/keras:dev-tx2-4.2_b158-py3

# this dockerfile is for Jetson tx2 jetpack 4.2
# to build:
# docker build -t lab04 -f Dockerfile.dev-tx2-4.2_b158 .
# to run:
# docker run --rm --privileged -p 8888:8888 -d lab04
# This should start Jupyter on port 8888 and print the container id
# to get the security token, wait 5-10 seconds then do:
# docker log <container id from above>
# access by pointing your browser to http://ip_of_your_tx2:8888
# use the token from above

# this dockerfile is experimental
# it should work, but watch your memory utilization!
# if this dies -- make sure you enable swap (see hw01)
WORKDIR /
RUN mkdir -p notebooks
WORKDIR notebooks

RUN wget https://s3-eu-west-1.amazonaws.com/darraghdog1/train.csv.zip 
RUN wget https://s3-eu-west-1.amazonaws.com/darraghdog1/w251_lab04_1dcnn.ipynb
RUN wget http://nlp.stanford.edu/data/glove.6B.zip
RUN unzip glove.6B.zip
