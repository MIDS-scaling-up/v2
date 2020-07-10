# Homework 5: TF2 and TF1

initial notes, keeping this the same, but moving to Xaiver NX and the new Nvidia images.
The 2 labs will be embedded into the the image.


## Introduction to Tensorflow v2
The idea of this homework is to serve as an introduction to [TensorFlow](https://www.tensorflow.org/).  TensorFlow 2 (TF2) was released in late 2019- and it includes [Keras](https://keras.io/), which you encountered in Session 4 and (hope you agree) is much easier to use.   

* Start the TF2 container: `sudo docker run -it --rm --runtime nvidia --network host hw5:latest`.  Note the ```--rm```:  when you type `exit`, this container will be removed from your device.
* Connect to your Jetson via browser on port 8888 and enter the passworld `nvidia`.
* Glance through the [TF2 beginner lab](https://www.tensorflow.org/tutorials/quickstart/beginner). This lab is available in the container at the path `/beginner.ipynb`.  Open up the notebook and run it to completion.  
* What's the structure of the network that's being used for classification? How good is it? Based on what you learned in homework 4, can you beat it? Hint: use something like [this](https://github.com/dragen1860/TensorFlow-2.x-Tutorials/tree/master/01-TF2.0-Overview) if you need an inspiration.
* Repeat for the [TF2 Quickstart lab](https://www.tensorflow.org/tutorials/images/transfer_learning_with_hub). This notebook is available on the container at `/transfer_learning_with_hub.ipynb`.  Open the notebook and run to completion on your Jetson.
* Note: you may have to make changes to the code and fix the OOM errors.  Hint: what is your batch size?
* Can you improve model accuracy? Hint: are your layers frozen?


## Introduction to / comparison with Tensorflow v1
TF2 is cool.  However, there's a lot of code still written in Tensorflow v1, and we think that some familiarity with it will still be useful. 
Please try to be patient and familiarize yourself with the code of this *beginner TF1* lab.  In our opinion definitely rough around the edges,  while at the same time representative of what you might encounter "in the wild".


The other concepts that we hope you will pick up are architectures for image classification as well as transfer learning.  The two go hand in hand: there are many pre-trained models today for image classification which you can further tweak (using transfer learning) on your own data. In this lab, you will see one approach where all the layers of the original model remain fixed.

Note also that we are doing this homework on the Jetson. It is powerful enough for real time inference - and even for incremental training.  This will come in handy later in the class as we begin to integrate neural processing into the kinds of pipelines you saw in homework 3.



### TensorFlow for Poets
In this section, we will generally follow the [Tensorflow for Poets lab](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0) at the Google CodeLabs.

Please read this before attempting the lab:

* To start an interactive TensorFlow container, run `sudo docker run -it --rm --runtime nvidia --network host nvcr.io/nvidia/l4t-tensorflow:r32.4.3-tf1.15-py3`. Note the ```--rm```:  when you type `exit`, this container will be removed from your device.
* You obviously don't need to install TensorFlow in the container explicitly (as the lab instructions suggest) ; it's already installed for you as a result of the Dockerfile instructions.
* In the command above, we allow the container to use the host's ports. Once you launch Tensorboard (step 4), you be able to connect to the Tensorboard instance by typing http://ipaddressofyourtx2:6006
* Remember to use python3 instead of regular python for all commands, since as we mentioned above, Nvidia no longer provides a TensorFlow distro for python2 as python2 is dead!
For example, instead of
```
python -m scripts.retrain -h
```
use
```
python3 -m scripts.retrain -h
```
And for the actual retraining, use
```
python3 -m scripts.retrain \
  --bottleneck_dir=tf_files/bottlenecks \
  --how_many_training_steps=500 \
  --model_dir=tf_files/models/ \
  --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}" \
  --output_graph=tf_files/retrained_graph.pb \
  --output_labels=tf_files/retrained_labels.txt \
  --architecture="${ARCHITECTURE}" \
  --image_dir=tf_files/flower_photos
```
* Once you are inside the interactive container, proceed to clone the TF for poets repository and proceed with 3+ sections of lab. Make sure you do all of the optional sections, except the "next steps" section 9.
* The Jetson packs a punch; make sure you run training for 4000 steps
* On x86 based systems, Nvidia provides a tool called "nvidia-smi" to monitor GPU utilization and performance in real time.  On the Jetson, this tool is not yet supported, unfortunately.  But, the Jetson community has developered another tool, jtop. <add install for that>


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
* The lab has another bug when you try to use the Inception model, because the [retrain.py](https://github.com/googlecodelabs/tensorflow-for-poets-2/blob/master/scripts/retrain.py), line 870, states:
```
resized_input_tensor_name = 'Mul:0'
```
whereas when MobileNet is used, line 912, we have
```
resized_input_tensor_name = 'input:0'
```
* Also observe lines 867 and 868 of [retrain.py](https://github.com/googlecodelabs/tensorflow-for-poets-2/blob/master/scripts/retrain.py)
```
input_width = 299
input_height = 299
```


### Questions:

1. What is TensorFlow? Which company is the leading contributor to TensorFlow?
1. What is TensorRT? How is it different from TensorFlow?
1. What is ImageNet? How many images does it contain? How many classes?
1. Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.
1. In your own words, what is a bottleneck?
1. How is a bottleneck different from the concept of layer freezing?
1. In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
1. How does a low `--learning_rate` (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?
1. How about a `--learning_rate` (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?
1. For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use [ImageNet](http://www.image-net.org/) images. How accurate was your model? Were you able to train it using a few images, or did you need a lot?
1. Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)?  Why?
1. Try the training again, but this time do `export ARCHITECTURE="inception_v3"` Are CPU and GPU training times different?
1. Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script?  Can we also glean the answer from examining TensorBoard?
```
python -m scripts.label_image --input_layer=??? --input_height=??? --input_width=???  --graph=tf_files/retrained_graph.pb --image=tf_files/flower_photos/daisy/21652746_cc379e0eea_m.jpg
```

### To turn in:
Turn in a text file or pdf with your answers to the questions above.
Please note that this homework is NOT graded, credit / nocredit only.
