# Homework 5 IS BEING REVISED AND WILL BE RELEASED SHORTLY.  SUMMER 2019 STUDENTS PLEASE HOLD OFF STARTING IT

## Introduction to Tensorflow
The idea of this lab is to serve as an introduction to [TensorFlow](https://www.tensorflow.org/).  TensorFlow is currently transitioning to [v2 alpha](https://www.tensorflow.org/alpha), which based on [Keras](https://keras.io/), which is much easier to use. However, there's a lot of code still written in Tensorflow v1, and we think that some hands-on experience with it will be useful. 

### TensorFlow container for TX2
First, you will need to build a Cuda Tensorflow container on your TX2.

First, build the docker container for [Nvidia TensorRT](https://developer.nvidia.com/tensorrt) using the corresponding Dockerfile [here](https://github.com/MIDS-scaling-up/v2/tree/master/backup/tensorrt)
```
# cd to the correct directory after git cloning the class repo
docker build -t tensorrt -f Dockerfile.tx2-4.2_b158 .
```

Now build the docker container for tensorflow using the python3 Dockerfile [here](https://github.com/MIDS-scaling-up/v2/tree/master/backup/tensorflow).  Note that at the moment, Nvidia provides no support for Tensorflow with python2 on the Jetson boards.
```
# cd to the correct directory after git cloning the class repo
docker build -t tensorflow -f Dockerfile.tx2-4.2_b158-py3 .
```

### TensorFlow for Poets
In this section, we will generally follow the [Tensorflow for Poets lab](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0) at the Google CodeLabs.

Please read this before attempting the lab:

* To start an interactive TensorFlow container, run `docker run --privileged --rm -p 6006:6006 -ti tensorflow bash`. Note the ```--rm```:  when you type `exit`, this container will be removed from your TX2.
* In the command above, 6006 is the port number that Tensorboard uses.  Once you launch Tensorboard (step 4), you be able to connect to the Tensorboard instance by typing http://ipaddressofyourtx2:6006
* Remember to use python3 instead of regular python for all commands, since as we mentioned above, Nvidia does not currently provide a TensorFlow distro for python2
* Once you are inside the interactive container, proceed to clone the TF for poets repository and proceed with 3+ sections of lab. Make sure you do all of the optional sections, except the "next steps" section 9.
* The Jetson packs a punch; make sure you run training for 4000 steps
* When you want to make sure the container does *not* see the GPU, run it as `docker run --rm -p 6006:6006 -ti tensorflow bash`, with no privileged flag
* On x86 based systems, Nvidia provides a tool called "nvidia-smi" to monitor GPU utilization and performance in real time.  On the Jetson, this tool is not yet supported, unfortunately.  But, the Jetpack has another tool, `/usr/bin/tegrastats`.  Its output looks like this:
```
root@tegra-ubuntu:~# tegrastats
RAM 2586/7846MB (lfb 1x1MB) CPU [0%@960,0%@499,0%@499,0%@959,0%@960,0%@960] EMC_FREQ 10%@665 GR3D_FREQ 53%@140 APE 150 MTS fg 0% bg 0% BCPU@41C MCPU@41C GPU@39C PLL@41C Tboard@35C Tdiode@37.75C PMIC@100C thermal@40.2C VDD_IN 3177/3177 VDD_CPU 536/536 VDD_GPU 383/383 VDD_SOC 536/536 VDD_WIFI 0/0 VDD_DDR 575/575
RAM 2586/7846MB (lfb 1x1MB) CPU [49%@806,10%@345,0%@345,46%@806,34%@959,26%@960] EMC_FREQ 10%@665 GR3D_FREQ 46%@140 APE 150 MTS fg 0% bg 0% BCPU@41C MCPU@41C GPU@39C PLL@41C Tboard@35C Tdiode@37.75C PMIC@100C thermal@40.2C VDD_IN 3177/3177 VDD_CPU 536/536 VDD_GPU 383/383 VDD_SOC 536/536 VDD_WIFI 0/0 VDD_DDR 575/575

```
GPU utilization can be deduced from the value of the GR3D_FREQ variable: the higher the value, the higher the GPU utilization.
* If you experience OOM (out of memory) errors, they could be related to the fact that the current port of Tensorflow does not understand the fact that the GPU memory that it sees is actually the same as the system memory and could be used for buffering.  Run the `flush_buffers.sh` script in this repo to help clear them out and re-run your tensorflow script.
* Another way to resolve the above is to add the following to the calling script:
```
config = tf.ConfigProto()
config.gpu_options.allow_growth = True

session = tf.Session(config=config, ...)
```
In the current version of the TF for poets lab, check out line 124 of [label_image.py](https://github.com/googlecodelabs/tensorflow-for-poets-2/blob/master/scripts/label_image.py)  This is where you'd need to make the change, e.g. add something like:
```
  # W251 insert
  config = tf.ConfigProto()
  config.gpu_options.allow_growth = True

#  with tf.Session(graph=graph) as sess:
  with tf.Session(graph=graph, config=config) as sess:
```
* The Google lab has another bug when you use the Inception model, because the [retrain.py](https://github.com/googlecodelabs/tensorflow-for-poets-2/blob/master/scripts/retrain.py), line 870, states:
```
resized_input_tensor_name = 'Mul:0'
```
whereas when MobileNet is used, line 912, we have
```
resized_input_tensor_name = 'input:0'
```
Also note lines 867 and 868 of [retrain.py](https://github.com/googlecodelabs/tensorflow-for-poets-2/blob/master/scripts/retrain.py)
```
input_width = 299
input_height = 299
```


### Questions:

1. What is TensorFlow? Which company is the leading contributor to TensorFlow?
1. What is TensorRT? How is it different from TensorFlow?
1. In your own words, what is a bottleneck?
1. In this lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
1. How does a low `--learning_rate` (step 7) value (like 0.005) affect the precision? How much longer does training take?
1. How about a `--learning_rate` (step 7) of 1.0? Is the precision still good enough to produce a usable graph?
1. For section 8, you can use any images you like. Pictures of food, people, or animals work well. You can even find images at ImageNet. How accurate was your model? Were you able to train it using a few images, or did you need a lot?
1. Run the script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)?
1. Try the training again, but this time do `export ARCHITECTURE="inception_v3"` Do you notice the CPU vs GPU difference now?
1. Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script?  Can we also glean the answer from examining TensorBoard?
```
python -m scripts.label_image --input_layer=??? --input_height=??? --input_width=???  --graph=tf_files/retrained_graph.pb --image=tf_files/flower_photos/daisy/21652746_cc379e0eea_m.jpg
```

### To turn in:
Turn in a text file or pdf with your answers to the questions above.

