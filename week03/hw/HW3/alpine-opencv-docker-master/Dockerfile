FROM resin/armhf-alpine:3.6 as build-stage

# Start cross-platform build
RUN [ "cross-build-start" ]

# Install tools and dependencies
RUN apk add -U --virtual=build-dependencies \
    build-base \
    clang \
    clang-dev ninja \
    cmake \
    freetype-dev \
    g++ \
    jpeg-dev \
    lcms2-dev \
    libffi-dev \
    libgcc \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    make \
    musl \
    musl-dev \
    openjpeg-dev \
    openssl-dev \
    python3-dev \
    zlib-dev \
    && apk add \
    curl \
    freetype \
    gcc \
    jpeg \
    libjpeg \
    openjpeg \
    python3 \
    tesseract-ocr \
    zlib

# Install Python dependencies
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pip3 install -U Pillow pytesseract numpy

# Clean Up
RUN apk del build-dependencies && \
    rm -rf /var/cache/apk/*

# End cross-platform build
RUN [ "cross-build-end" ]

FROM resin/armhf-alpine:3.6

# Start cross-platform build
RUN [ "cross-build-start" ]

# Install Python3
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    rm -r /.dockerenv

# Add symbolic links to for Python3
RUN ln -s /usr/bin/python3 /usr/local/bin/python && \
    ln -s /usr/bin/pip3 /usr/local/bin/pip && \
    pip install --upgrade pip

# Copy dependencies from build stage
# COPY --from=build-stage /usr/local/lib /usr/local/lib     # <-- if adding more libraries in the build stage you probably want to re-enable this
COPY --from=build-stage /usr/lib/lib*.so.* /usr/lib/
COPY --from=build-stage /usr/lib/python3.6/site-packages/ /usr/lib/python3.6/site-packages/

ENV CGO_CPPFLAGS -I/usr/local/include
ENV CGO_CXXFLAGS "--std=c++1z"
ENV CGO_LDFLAGS "-L/usr/local/lib -lopencv_core -lopencv_face -lopencv_videoio -lopencv_imgproc -lopencv_highgui -lopencv_imgcodecs -lopencv_objdetect -lopencv_features2d -lopencv_video -lopencv_dnn -lopencv_xfeatures2d -lopencv_plot -lopencv_tracking"

# Add pre-built OpenCV
ADD opencv-prebuilt/cv2.so /usr/lib/python3.6/site-packages/cv2.so
ADD opencv-prebuilt/include-opencv /usr/local/include/opencv
ADD opencv-prebuilt/include-opencv2 /usr/local/include/opencv2
ADD opencv-prebuilt/local-lib /usr/local/lib

# Add the application and its dependent modules
ADD demo/corner-demo.py /home
ADD demo/chessboard.jpg /home

# End cross-platform build
RUN [ "cross-build-end" ]
