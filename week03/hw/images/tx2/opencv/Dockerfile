FROM cudabase:latest

RUN mkdir -p /app
WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
ENV TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
Run apt-get update \
  && apt-get install -y --no-install-recommends python3-opencv \
  && apt-get install -y python3-pip \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install paho-mqtt

