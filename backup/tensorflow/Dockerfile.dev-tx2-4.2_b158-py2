FROM w251/tensorrt:dev-tx2-4.2_b158

RUN apt update && apt install -y python-pip

RUN apt install -y zlib1g-dev zip libjpeg8-dev libhdf5-dev
RUN pip install -U numpy grpcio absl-py py-cpuinfo psutil portpicker grpcio six mock requests gast h5py astor termcolor

RUN pip install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow-gpu
