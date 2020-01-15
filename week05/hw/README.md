# Homework 5

## Introduction to Tensorflow
The idea of this lab is to servce as an introduction to [TensorFlow](https://www.tensorflow.org/).  TensorFlow as moved to a new version based on [Keras](https://keras.io/), which you encountered in Session 4 and (hope you agree) is much easier to use.  

Please try to be patient and familiarize yourself with the code of this *beginner* lab.  In our opinion definitely rough around the edges,  while at the same time representative of what you might encounter "in the wild".


The other concepts that we hope you will pick up are architectures for image classification as well as transfer learning.  The two go hand in hand: there are many pre-trained models today for image classification which you can further tweak (using transfer learning) on your own data. In this lab, you will see one approach where all the layers of the original model remain fixed.

Note also that we are doing this homework on the TX2. It is powerful enough for real time inference - and even for incremental training.  This will come in handy later in the class as we begin to integrate neural processing into the kinds of pipelines you saw in homework 3.


### TensorFlow container for TX2
First, you will need to build a Cuda Tensorflow container on your TX2.

First, build the container using the Dockerfile located in this [directory](https://github.com/MIDS-scaling-up/v2/tree/rdejana_hw5/week05/hw/Dockerfile.hw5).

```
# cd to the correct directory after git cloning the class repo
docker build -t hw5 -f Dockerfile.hw5 .
```
Note that at the moment, Nvidia provides no support for Tensorflow with python2 on the Jetson boards.

### Transfer learning with TensorFlow Hub
In this section, we will generally follow the [Tensorflow for Poets lab](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0) at the Google CodeLabs.

Please read this before attempting the lab:

* To start the TensorFlow container, run `docker run --privileged --rm -p 8888:8888 -d tensorflow`. Note the ```--rm```:  when you type stop the container, this container will be removed from your TX2.



* On x86 based systems, Nvidia provides a tool called "nvidia-smi" to monitor GPU utilization and performance in real time.  On the Jetson, this tool is not yet supported, unfortunately.  But, the Jetpack has another tool, `/usr/bin/tegrastats`.  Its output looks like this:
```
root@tegra-ubuntu:~# tegrastats
RAM 2586/7846MB (lfb 1x1MB) CPU [0%@960,0%@499,0%@499,0%@959,0%@960,0%@960] EMC_FREQ 10%@665 GR3D_FREQ 53%@140 APE 150 MTS fg 0% bg 0% BCPU@41C MCPU@41C GPU@39C PLL@41C Tboard@35C Tdiode@37.75C PMIC@100C thermal@40.2C VDD_IN 3177/3177 VDD_CPU 536/536 VDD_GPU 383/383 VDD_SOC 536/536 VDD_WIFI 0/0 VDD_DDR 575/575
RAM 2586/7846MB (lfb 1x1MB) CPU [49%@806,10%@345,0%@345,46%@806,34%@959,26%@960] EMC_FREQ 10%@665 GR3D_FREQ 46%@140 APE 150 MTS fg 0% bg 0% BCPU@41C MCPU@41C GPU@39C PLL@41C Tboard@35C Tdiode@37.75C PMIC@100C thermal@40.2C VDD_IN 3177/3177 VDD_CPU 536/536 VDD_GPU 383/383 VDD_SOC 536/536 VDD_WIFI 0/0 VDD_DDR 575/575

```
GPU utilization can be deduced from the value of the GR3D_FREQ variable: the higher the value, the higher the GPU utilization.
* If you experience OOM (out of memory) errors, they could be related to the fact that the current port of Tensorflow does not understand the fact that the GPU memory that it sees is actually the same as the system memory and could be used for buffering.  Run the `flush_buffers.sh` script in this repo to help clear them out and re-run your tensorflow script.

## Part 1: TensorFlow, Tensor Hub, and Transfer Learning.
1. This part uses a notebook to demonstate transfer learning.  You'll need you to first get your token.

```
$docker logs tensorflow
[I 16:11:29.070 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 16:11:30.208 NotebookApp] Serving notebooks from local directory: /notebooks
[I 16:11:30.208 NotebookApp] The Jupyter Notebook is running at:
[I 16:11:30.208 NotebookApp] http://7d783a4b0feb:8888/?token=0cebf472b557f2e871de6be4e0717ff35cdd30b013b0d7e5
[I 16:11:30.209 NotebookApp]  or http://127.0.0.1:8888/?token=0cebf472b557f2e871de6be4e0717ff35cdd30b013b0d7e5
[I 16:11:30.209 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation)
```
and point your browser to http://yourjetsonip:8888?token=yourtoken

2. Select the file `transfer_learning_with_hub.ipynb`
1. This lab uses TensorFlow to download models.  This example is using 'https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2'.  Navigate to this url and notice the following:
```
For this module, the size of the input image is fixed to height x width = 224 x 224 pixels. The input images are expected to have 3 RGB color values in the range [0,1], 
```
Take notice of where the lab specifies this.  Other models, e.g. 'https://tfhub.dev/google/tf2-preview/inception_v3/classification/4', may use a different image size.

4. Run to the 'Simple transfer learning' section.  Think about the following, how was the prediction formated?  How did is the prediction with the highest probability?  How is the prediction mapped to a class name?

## Part 2: CLI
1. In part 1, you used a simple notebook to train an image classifier with TensorFlow, Tensor Hub, and Transfer Learning.  Now, you will run create a classification model using a CLI utility called [make_image_classifier](https://github.com/tensorflow/hub/tree/master/tensorflow_hub/tools/make_image_classifier).  Make sure you docker image from part 1 is running (if not, start it again) and access the shell with the following command
```
docker exec -it tensorflow bash
```
2. create a working direction, say `/notebooks/part2` and change to the directory.
```
mkdir /notebooks/part2
cd /notebooks/part2
```
3. With this utility, it is possilbe to train on any image dataset using the --image-dir option.  The directory specified by --image-dir is a directory of subdirectories of images, defining the classes you want your model to distinguish. Say you wanted to classify your photos of pets to be cat, dog or rabbit. Then you would arrange JPEG files of such photos in a directory structure like:
```
my image_dir
|-- cat
|   |-- a_feline_photo.jpg
|   |-- another_cat_pic.jpg
|   `-- ...
|-- dog
|   |-- PuppyInBasket.JPG
|   |-- walking_the_dog.jpeg
|   `-- ...
`-- rabbit
    |-- IMG87654321.JPG
    |-- my_fluffy_rabbit.JPEG
    `-- ...
```
For now, you'll omit the --image-dir and the utility will use the TF flowers dataset.

Run the command: 
```
make_image_classifier \
 --tfhub_module https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4  \
 --image_size 224   \
 --saved_model_dir output/new_model   \
 --labels_output_file class_labels.txt   \
 --train_epochs 50 \
 --batch_size 10
 ```
 where -tfhub_module is the URL of a pre-trained model on TF Hub, --image_size is the size images are resized to, --saved_model_dir is the directory to save the trained move to, --labels_output_file  is the text file where the class labels are saved to, one per line, in the same order as they appear in the predictions output by the model, --train_epochs is the number of epochs, and --batch_size is the how many images are sampled each training step.  Additional flags may be found by running the command ``make_image_classifier --helpfull``

4. To test your model, you'll need to write a simple python script that uses the model for inference.  This script should take your model, the classes, and a test image as input and return the top 3 predictions, both the probablity and classname.

5. Try training with a dataset of your choice.  Pictures of food, people, or animals work well. You can even use [ImageNet](http://www.image-net.org/) images. 

You may find additional example at https://www.tensorflow.org/tutorials/images.

## Part 3 Simple Object Detection (Optional)
1. The first two parts covered ways of building an image classifier while this part shows how you can use Tensorflow for object detection.  Make sure your tensorflow image is running and open your brower to ``http://yourjetsonip:8888?token=yourtoken``
1. Select the file ``object_detection.ipynb``
2. Run the notebook with the defaults.
### Questions:

1. What is TensorFlow? Which company is the leading contributor to TensorFlow?
1. What is TensorRT? How is it different from TensorFlow?
1. What is ImageNet? How many images does it contain? How many classes?
1. Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.
1. In your own words, what is a bottleneck?
1. How is a bottleneck different from the concept of layer freezing?
1. In part one this lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
1. Why is the batch size important?  What happens if you try running with a batch size of 32?  What about a batch size of 4?
1. Find another image classification feature vector from tfhub.dev and rerun the notebook.  Which one did you pick and what changes, if any did you need to make?
1. How long did the training take in part 2?

1. In part 2, you can also specifiy the learning rate using the flag `--learning_rate`.   How does a low `--learning_rate` (part 2, step  4) value (like 0.001) affect the precision? How much longer does training take?
1. How about a `--learning_rate` (part 2, step  4) of 1.0? Is the precision still good enough?
1. For part 2, step 5,  How accurate was your model? Were you able to train it using a few images, or did you need a lot?
1. What is the difference between image classification and object detection?
1. In part 3, which model ran faster, FasterRCNN+InceptionResNet V2 or ssd+mobilenet V2.  how much so?  Which was more accurate? 



### To turn in:
Turn in a text file or pdf with your answers to the questions above.
Please note that this homework is NOT graded, credit / nocredit only.
