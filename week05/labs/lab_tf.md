# Mnist with Tensorflow

In this lab, we will train a convolutional neural network on the MNIST data set using Tensorflow.
Please follow these general steps:
* Clone this repo into a directory on your Jetson.  If you cloned it before, do a git pull
* Start up an interactive Tensorflow-python3 docker container, passing port 6006 and the directory that you cloned the class to.  It should look something like this:
```
docker run --rm -p 6006:6006 -v /home/nvidia/v2:/v2 -ti w251/tensorflow:tx2-3.3_b39-py3 bash
```
* go to the lab5 directory - e,g, cd /v2/week05/labs .  Here, you can run the training script, e.h.
```
python3 mnist.py
```
* Can you fix the code to ensure that it finds the data it needs?
* How long does the script need to complete?
* How many cores does it take?
* What is an epoch?
* How many epochs do we train for?
* What is our loss function
* What is our learning rate?
* What is our batch size?
* What happens if we double the learning rate?
* Does the model overfit?
* Can you examine the training results in Tensorboard?
* Can you repeat the lab on the GPU?

```

