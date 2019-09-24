FROM python:3.6.8-alpine3.8

RUN apk --update add --virtual=.build-dependencies \
	mosquitto \
	mosquitto-clients \
	python-dev \
	build-base \
	wget && \
	pip install paho-mqtt && \
	apk del .build-dependencies



	
WORKDIR /
COPY . .
CMD ["python", "./tx2_broker.py"]
