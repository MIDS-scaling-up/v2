## Run time inference for Image Classification and Object Detection using TensorFlow and TensorRT

### Introduction
In this  lab, you will learn how to speed up TensorFlow models at inference time with Nvidia's runtime accelerator, TensorRT.  The lab generally follows 
[this tutorial](https://github.com/NVIDIA-AI-IOT/tf_trt_models). Please spend some time reading through this page. TensorRT 
provides its own runtime environment, but in this tutorial, it is just used to optimize an existing frozen TensorFlow graph, reducing it from 32-bit precision to 16-bit precision. The optimized graph is loaded into the Tensorflow runtime at inference time.

### Setup

Our TX2 docker container is built on the Keras + TF + TensoRT container you may have seen earlier in the class (please peek inside
the Dockerfile):
```
docker build -t tensorrtlab05 -f Dockerfile.tensorrtlab05 .
```
Once this completes, let's launch the container:
```
docker run --privileged --rm -p 8888:8888 -d tensorrtlab05
```
If for whatever reason you were unable to get your container built, just use our pre-built version:
```
docker run --privileged --rm -p 8888:8888 -d w251/tensorrtlab05:dev-tx2-4.2_b158
```
As before, find the token using ```docker logs``` and use it to connect to your jupyter notebook at http://jetsonip:8888

### Image Classification
Complete the Image Classication Example under examples/classification, then try the following:
1. Can you modify the notebook to measure the time it takes for one forward pass?
1. Can you measure the time it takes for one forward pass using pure TensorFlow (hint: use the original frozen graph object rather than the TensorRT optimized one)

### Object Detection
Complete the Object Detection example under examples/detection and answer the questions above as well.  There's a slight bug in cell 11, can you fix it?
