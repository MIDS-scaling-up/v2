# Remember to change the username and API key values in the <> to your own values!
# AUTHOR chenbryanchen@gmail.com
FROM ubuntu:16.04

RUN apt-get update 

RUN apt-get install -y \
    python \
    python-pip \
    python-setuptools \
    python-dev \ 
    openssh-client \
    openssh-server \

RUN pip install SoftLayer

RUN echo '[softlayer]' > ~/.softlayer

RUN echo 'username = <YOUR_SL_API_ID>' >> ~/.softlayer

RUN echo 'api_key = <YOUR_SL_API_KEY>' >> ~/.softlayer

RUN echo 'endpoint_url = https://api.softlayer.com/xmlrpc/v3.1/' >> ~/.softlayer

RUN ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""

ENTRYPOINT ["/bin/bash"]
