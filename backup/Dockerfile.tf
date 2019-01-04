FROM tensorrt

RUN apt update && apt install -y python-pip

RUN pip install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp33 tensorflow-gpu
