## Run time inference for Image Classification using PyTorch and EfficientNet

### Introduction
In this nano lab, you will learn how to do inference with PyTorch and EfficientNet

### Setup

Our TX2 docker container is built on the PyTorch container you may have seen earlier in the class (please peek inside
the Dockerfile):
```
docker build -t pytorchlab05 -f Dockerfile.pytorchlab05 .
```
Once this completes, let's launch the container:
```
docker run --privileged --rm -p 8886:8888 -d pytorchlab05
```
If for whatever reason you were unable to get your container built, just use our pre-built version:
```
docker run --privileged --rm -p 8888:8888 -d w251/pytorchlab05:dev-tx2-4.3_b132
```
As before, find the token using ```docker logs``` and use it to connect to your jupyter notebook at http://jetsonip:8888

### Image Classification using pre-trained weights
In your Jupyter notebook, navigate to EfficientNet-Pytorh folder, examples, simple, and run example.ipynb

### Notes:
If you see an error message related to PIL, please open a terminal in jupyter and type ```pip3 install 'pillow<7'```
