FROM ubuntu:16.04

RUN apt-get update 

RUN apt-get install -y \
    python \
    python-pip \
    python-setuptools \
    python-dev \ 
    openssh-client \
    openssh-server

RUN pip install SoftLayer

RUN echo '[softlayer]' > ~/.softlayer

RUN echo 'username = bchen18' >> ~/.softlayer

RUN echo 'api_key = a29dbfd9b4d160c7e81fd22b2dfd8d23ea998c740dffb8d4a4ad48ad9703878e' >> ~/.softlayer

RUN echo 'endpoint_url = https://api.softlayer.com/xmlrpc/v3.1/' >> ~/.softlayer

RUN ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""

ENTRYPOINT ["/bin/bash"]
