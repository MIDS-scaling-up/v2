FROM nvcr.io/nvidia/tensorflow:19.01-py3
MAINTAINER ggrunin@gmail.com

RUN apt-get update \
 && apt-get install -y --no-install-recommends sudo openssh-server \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd 



ADD .ssh /root/.ssh


# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd


COPY start.sh  /root/
WORKDIR /root
RUN chmod +x ./start.sh

RUN cd /opt && git clone https://github.com/NVIDIA/OpenSeq2Seq && cd /opt/OpenSeq2Seq && pip install -r requirements.txt


CMD ["./start.sh"]
