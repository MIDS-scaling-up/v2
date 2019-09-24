FROM python:3-alpine3.7

#RUN echo -e '@edgunity http://nl.alpinelinux.org/alpine/edge/community\n\
#@edge http://nl.alpinelinux.org/alpine/edge/main\n\
#@testing http://nl.alpinelinux.org/alpine/edge/testing\n\
#@community http://dl-cdn.alpinelinux.org/alpine/edge/community'\
#  >> /etc/apk/repositories

RUN apk add --update --no-cache \
	--virtual=.build-dependencies \
	build-base \
	openblas-dev \
	unzip \
	wget \
	cmake \
	libjpeg \
	libjpeg-turbo-dev \
	jasper-dev \
	tiff-dev \
	libwebp-dev \
	clang-dev \
	linux-headers \
	&& pip install numpy

ENV CC /usr/bin/clang
ENV CXX /usr/bin/clang++

ENV OPENCV_VERSION=3.1.0

RUN mkdir /opt && cd /opt && \
  wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip && \
  unzip ${OPENCV_VERSION}.zip && \
  rm -rf ${OPENCV_VERSION}.zip

RUN mkdir -p /opt/opencv-${OPENCV_VERSION}/build && \
	cd /opt/opencv-${OPENCV_VERSION}/build && \
	cmake \
	-D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D WITH_FFMPEG=NO \
	-D WITH_IPP=NO \
	-D WITH_OPENEXR=NO \
	-D WITH_TBB=YES \
	-D BUILD_EXAMPLES=NO \
	-D BUILD_ANDROID_EXAMPLES=NO \
	-D INSTALL_PYTHON_EXAMPLES=NO \
	-D BUILD_DOCS=NO \
	-D BUILD_opencv_python2=NO \
	-D BUILD_opencv_python3=ON \
	-D PYTHON3_EXECUTABLE=/usr/local/bin/python \
	-D PYTHON3_INCLUDE_DIR=/usr/local/include/python3.6m/ \
	-D PYTHON3_LIBRARY=/usr/local/lib/libpython3.so \
	-D PYTHON_LIBRARY=/usr/local/lib/libpython3.so \
	-D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.6/site-packages/ \
	-D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python3.6/site-packages/numpy/core/include/ \
	.. && \
	make VERBOSE=1 && \
	make && \
	make install && \
	rm -rf /opt/opencv-${OPENCV_VERSION}

WORKDIR /src/app
COPY . .
CMD ["python", "./video_read.py"]
