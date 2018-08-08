FROM caffealt

# AUTHOR chenbryanchen@gmail.com

# Install dependencies
WORKDIR /
RUN apt-get install -y cmake git gstreamer1.0-plugins-good libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libglew-dev && git clone http://github.com/dusty-nv/jetson-reinforcement
WORKDIR jetson-reinforcement
RUN git submodule update --init

# Fix CMake files
RUN sed -i -e 's/apt-get install -y/apt-get install/g' CMakePreBuild.sh && sed -i -e 's/apt-get install/apt-get install -y/g' CMakePreBuild.sh
RUN sed -i '32,39d' CMakePreBuild.sh && sed -i '32i sudo apt-get install -y gazebo7 libgazebo7-dev' CMakePreBuild.sh
RUN sed -i '68,75d' CMakePreBuild.sh && sed -i '68i sudo apt-get install -y ipython ipython-notebook; sudo pip install jupyter' CMakePreBuild.sh

# Build
RUN mkdir build
WORKDIR build
RUN cmake ../
RUN make

# Install Jupyter
RUN apt-get install -y libzmq3-dev && python -m pip install jupyter
