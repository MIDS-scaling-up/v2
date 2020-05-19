# Homework 4 Part 2

## Overview
This Homework will compare image classificaiton inference performance with Tensorflow 1.15, Tensorflow 2, TFLite, and Jetson Inference.  Note, this is not currently containerized.

## Reading
- https://www.tensorflow.org/lite/performance/post_training_quantization
- https://devblogs.nvidia.com/speeding-up-deep-learning-inference-using-tensorrt/

## Framework installation
When running on a TX2, run `sudo jetson_clocks` to improve performance.

## Classification images
Find at least 3 images on your own to use for classification.  
You will be submitting these images as part of the homework.

### Prerequisites 
1. Install system packages
```
$ sudo apt-get update
$ sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
```
2. Install and upgrade pip3
``
$ sudo apt-get install python3-pip
``
3. Install Virtualenv
```
$ sudo pip3 install -U virtualenv # system-wide install
```
4. Create the virtualenv directory under /data
```
$ cd /data
$ mkdir virtualenvs
```

 If you /data directory is owned by root, create using sudo, `sudo mkdir virtualenvs` and then change ownership to your id, `sudo chown -R $USER:$USER virtualenvs`
### TFLite
1. Create a TFLite python3 virtualenv in your /data directory. 
```
$ cd /data/virtualenvs
$ virtualenv -p python3 ./tflite
```
 2. Activate virtual enviroment.  This is importand as TFLite will only be available when using this virtual environment. 
 ```
 $ source /data/virtualenvs/tflite/bin/activate
 ```
 3. Install TFLite runtime and additional components. 
 Open https://www.tensorflow.org/lite/guide/python and look for the latest version that supports ARM 64 at your version of python.  Currently this is https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_aarch64.whl
 ```
 pip3 install testresources setuptools
 pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_aarch64.whl
 pip3 install Pillow numpy
 ```
 4. Deactivate virtualenv
 ```
 deactiate
 ```
### Tensorflow 1.15
1. Create a TF 1.15 python3 virtualenv in your /data directory. 
```
$ cd /data/virtualenvs
$ virtualenv -p python3 ./tf115
```
2. . Activate virtual enviroment.  This is importand as TF 1.15 will only be available when using this virtual environment. 
 ```
 $ source /data/virtualenvs/tf115/bin/activate
 ```
3. Install TF 1.15 runtime and additional components.
```
pip3 install  testresources setuptools
pip3 install numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 'tensorflow<2'
pip3 install --upgrade tensorflow-hub
pip3 install Pillow
```
Full instructions may be found at https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html

### Tensorflow 2.x
1. Create a TF 1.15 python3 virtualenv in your /data directory. 
```
$ cd /data/virtualenvs
$ virtualenv -p python3 ./tf2
```
2. . Activate virtual enviroment.  This is importand as TF 2 will only be available when using this virtual environment. 
 ```
 $ source /data/virtualenvs/tf2/bin/activate
 ```
3. Install TF 1.15 runtime and additional components.
```
pip3 install  testresources setuptools
pip3 install numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 keras-preprocessing>=1.1.0 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow
pip3 install --upgrade tensorflow-hub
pip3 install Pillow
```
Full instructions may be found at https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html

### Jetson Inference

Here's a condensed form of the commands to download, build, and install the project:
```
cd /data
sudo apt-get update
sudo apt-get install git cmake libpython3-dev python3-numpy
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
cmake ../
make -j$(nproc)
sudo make install
sudo ldconfig

```
Note, if your permissions prevent creating a directory under /data, run the folloing instead of the git clone.
```
sudo git clone --recursive https://github.com/dusty-nv/jetson-inference
sudo chown -R $USER:$USER jetson-inference
```
Don't worry about which models are downloaded as you'll be downloading later on.


## Assignment 
Clone this repository to your TX2.  

## Part 1: TFLite
In this part, you'll run a simple image classificaiton example against a sample image and your classification test images.  You'll need to run against each of the supplied models, running the classification at least 5 times, returning the (up to) top 5 results.
1. Enable your tflite virtualenv.
2. cd to tflite.
3. Run to following 
```
    python3 classify_image.py --model models/<modelName>  --labels models/imagenet_labels.txt   --input <pathToImage> -k 5
``` 
For each of the following models:
- efficientnet-L_quant.tflite
- efficientnet-M_quant.tflite
- efficientnet-S_quant.tflite
- inception_v4_299_quant.tflite
- mobilenet_v1_1.0_224_quant.tflite
- mobilenet_v2_1.0_224_quant.tflite

using the test image `images/parrot.jpg` and your test images.

### Questions
1. What was the average inference time for model and image combination?  What where the returned classes their score?
2. In your opinion, which model is best and why?

## Part 2: TensorFlow 1.15
In this part, you'll run a simple image classificaiton example against a sample image and your classification test images.  You'll need to run against each of the supplied models, running the classification at least 5 times, returning the (up to) top 5 results.

1. Enable your tf115 virtualenv
2. cd to tf1.15
3. Run the following
```
    python3 classifier.py -m <modelURL> -i <image>
```

This classifier downloads models from TensorFlow Hub.  Downloads are not cached and are redowned with each run.

Test with the following, passing the URL as the -m parameter
- mobilenet_v1_100_224 URL: https://tfhub.dev/google/imagenet/mobilenet_v1_100_224/classification/4
- mobilenet_v2_130_224 URL: https://tfhub.dev/google/imagenet/mobilenet_v2_130_224/classification/4 
- efficientnet b0 URL: https://tfhub.dev/google/efficientnet/b0/classification/1
- efficientnet b4 URL: https://tfhub.dev/google/efficientnet/b4/classification/1
- efficientnet b7 URL: https://tfhub.dev/google/efficientnet/b7/classification/1

using the test image `images/parrot.jpg` and your test images.

For the EfficientNet models, please read the Usage section carefully. 

If you are seeing memory errors when running, run the flush_buffers.sh script located in the tf115 directory. 
```
sudo sh flush_buffers.sh
```
### Questions
3. Did the EfficientNet models return the correct classifiction?  If not why, and how would you fix this?
4. How big (in megabytes) are the models? 
5. How did the performance compare to TFLite?  Be sure to through out the first run as it includes downloading.

## Part 3: TensorFlow 2
Repeat the same tests you did for TF 1.15.  You'll want to copy the `classifier.py` file from the tf1.15 directory.
1. Enable your tf115 virtualenv
2. cd to tf2
3. cp ../tf1.15/classifier.py ./
4. Update classifier.py to work with TF 2.
Please note, TF 2 does not support the tfhub call 
```
IMAGE_SHAPE = (height, width)
        classifier = tf.keras.Sequential([
            hub.KerasLayer(module, input_shape=IMAGE_SHAPE+(3,))])
```
You'll need to find another way to set the imput image dimensions.  The required values may be found at the model's URL.

Test with the following, passing the URL as the -m parameter
- mobilenet_v1_100_224 URL: https://tfhub.dev/google/imagenet/mobilenet_v1_100_224/classification/4
- mobilenet_v2_130_224 URL: https://tfhub.dev/google/imagenet/mobilenet_v2_130_224/classification/4 
- efficientnet b0 URL: https://tfhub.dev/google/efficientnet/b0/classification/1
- efficientnet b4 URL: https://tfhub.dev/google/efficientnet/b4/classification/1
- efficientnet b7 URL: https://tfhub.dev/google/efficientnet/b7/classification/1

using the test image `images/parrot.jpg` and your test images.

If you are seeing memory errors when running, run the flush_buffers.sh script located in the tf115 directory. 
```
sudo sh flush_buffers.sh
```
### Questions
6. Compare the performance of TF2 to TF 1.15

## Part 4: Jetson Inference.
In this part, you'll work with Jeton Inference.  


1. cd to jetsoninference
2. Down load at least 4 classifcation models and take note of which ones.  This is done via the following command
```
./download-models.sh YES
```
You only need to download classification models. If possible, it is easier to download all the classification and choose which ones to test. 
3. Run the test program to verify that jetson inference is working correctly.  Be sure to run with python3.
The first time your run with a new model, it will take some time to process it.
```
python3 imagenet-console.py --network=googlenet images/parrot.jpg out.jpg
```

Classification Networks

| Network       | CLI argument   | NetworkType enum |
| --------------|----------------|------------------|
| AlexNet       | `alexnet`      | `ALEXNET`        |
| GoogleNet     | `googlenet`    | `GOOGLENET`      |
| GoogleNet-12  | `googlenet-12` | `GOOGLENET_12`   |
| ResNet-18     | `resnet-18`    | `RESNET_18`      |
| ResNet-50     | `resnet-50`    | `RESNET_50`      |
| ResNet-101    | `resnet-101`   | `RESNET_101`     |
| ResNet-152    | `resnet-152`   | `RESNET_152`     |
| VGG-16        | `vgg-16`       | `VGG-16`         |
| VGG-19        | `vgg-19`       | `VGG-19`         |
| Inception-v4  | `inception-v4` | `INCEPTION_V4`   |


4. Write a python program that performs image classificaiton example against the sample image and your classification test images.  You'll need to run against each of the downloaded models, running the classification at least 5 times. Use `imagenet-console.py` as an example. 

Be sure to use the test image `images/parrot.jpg` and your test images.

### Questions
7. What models did you use?
8. What was the average inference time for model and image combination?  What where the returned classes their score?


### Final Questions
9. In your own words, what is quanization? What is effect on peformance and accuracy?
10. In your option, which framework was best?  Why?

## What to submit
- Your answers to all questions
- Your test images
- Any updates you made to the TF 1.15 classifer.
- Your TF 2.0 classifer.
- Your Jetson Inference classifer

