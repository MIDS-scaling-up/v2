FROM arm64v8/ubuntu:18.04

## Install some dependencies
RUN apt-get update && apt-get install -y \
      libtbb-dev \
      qt5-default \
      libgstreamer1.0-0 \
      gstreamer1.0-plugins-base \
      gstreamer1.0-plugins-good \
      gstreamer1.0-plugins-bad \
      gstreamer1.0-plugins-ugly \
      gstreamer1.0-libav \
      gstreamer1.0-doc \
      gstreamer1.0-tools \
      gstreamer1.0-x \
      gstreamer1.0-alsa \
      gstreamer1.0-gl \
      gstreamer1.0-gtk3 \
      gstreamer1.0-qt5 \
      gstreamer1.0-pulseaudio \
      libv4l-dev \
      libcurl4 \ 
      curl \
      git

# Installed opencv precompiled version on jetson
ADD opencv-3.4.3.tar.gz /

WORKDIR /opendatacam
