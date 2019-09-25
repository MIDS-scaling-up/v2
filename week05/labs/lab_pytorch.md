## Run time inference for Image Classification using PyTorch and EfficientNet

### Introduction
In this  lab, you will learn how to speed up TensorFlow models at inference time with Nvidia's runtime accelerator, TensorRT.  The lab generally follows 
[this tutorial](https://github.com/NVIDIA-AI-IOT/tf_trt_models). Please spend some time reading through this page. TensorRT 
provides its own runtime environment, but in this tutorial, it is just used to optimize an existing frozen TensorFlow graph, reducing it from 32-bit precision to 16-bit precision. The optimized graph is loaded into the Tensorflow runtime at inference time.

### Setup

Our TX2 docker container is built on the Keras + TF + TensoRT container you may have seen earlier in the class (please peek inside
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
docker run --privileged --rm -p 8888:8888 -d w251/tensorrtlab05:dev-tx2-4.2.1_b97
```
As before, find the token using ```docker logs``` and use it to connect to your jupyter notebook at http://jetsonip:8888

### Image Classification
In your Jupyter notebook, navigate to EfficientNet-Pytorh folder, examples, simple, and run example.ipynb
