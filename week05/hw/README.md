# Homework 5

## Tensorflow for Poets

For this homework, you need to install Tensorflow on your TX2.

Build the docker container for tensorrt using the Dockerfile [here](https://github.com/MIDS-scaling-up/v2/tree/master/backup/tensorrt)
```
# cd to the correct directory after git cloning the class repo
docker build -t tensorrt -f Dockerfile.tx2-3.3_b39
```

Now build the docker container for tensorflow using the python2 Dockerfile [here](https://github.com/MIDS-scaling-up/v2/tree/master/backup/tensorflow).
```
# cd to the correct directory after git cloning the class repo
docker build -t tensorflow -f Dockerfile.tx2-3.3_b39-py2 .
```


Complete the [Tensorflow for Poets lab](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0) at the Google CodeLabs. Make sure you do all of the optional sections (except section 9).

### Notes specific to our Jetson setup:
* to start an interactive TensorFlow container, run `docker run --privileged --rm -p 6006:6006 -ti tensorflow bash`.  When you type `exit`, this container will be removed from your TX2.
* In the command above, 6006 is the port number that Tensorboard uses.  Once you start training, will be able to connect to the Tensorboard instance by typing http://ipaddressofyourtx2:6006
* Once you are inside the container, install git by typing `apt install -y git` , then you can proceed to clone the TF for poets repository and with the rest of the lab
* The Jetson packs a punch; make sure you run training for 4000 steps
* To make sure the container does not see the GPU, run it as `docker run --rm -p 6006:6006 -ti tensorflow bash`, with no privileged flag
* On x86 based systems, Nvidia provides a tool called "nvidia-smi" to monitor GPU utilization and performance in real time.  On the Jetson, this tool is not yet supported, unfortunately.  But, the Jetpack has another tool, `/home/nvidia/tegrastats`.  Its output looks like this:
```
root@tegra-ubuntu:~# ./tegrastats
RAM 2586/7846MB (lfb 1x1MB) CPU [0%@960,0%@499,0%@499,0%@959,0%@960,0%@960] EMC_FREQ 10%@665 GR3D_FREQ 53%@140 APE 150 MTS fg 0% bg 0% BCPU@41C MCPU@41C GPU@39C PLL@41C Tboard@35C Tdiode@37.75C PMIC@100C thermal@40.2C VDD_IN 3177/3177 VDD_CPU 536/536 VDD_GPU 383/383 VDD_SOC 536/536 VDD_WIFI 0/0 VDD_DDR 575/575
RAM 2586/7846MB (lfb 1x1MB) CPU [49%@806,10%@345,0%@345,46%@806,34%@959,26%@960] EMC_FREQ 10%@665 GR3D_FREQ 46%@140 APE 150 MTS fg 0% bg 0% BCPU@41C MCPU@41C GPU@39C PLL@41C Tboard@35C Tdiode@37.75C PMIC@100C thermal@40.2C VDD_IN 3177/3177 VDD_CPU 536/536 VDD_GPU 383/383 VDD_SOC 536/536 VDD_WIFI 0/0 VDD_DDR 575/575

```
GPU utilization cab be deduced from the value of the GR3D_FREQ variable: the higher the value, the higher the GPU utilization.
* If you experience OOM (out of memory) errors, they could be related to the fact that the current port of Tensorflow does not appreciate the fact that the GPU memory that it sees is actually the same as the system memory and could be used for buffering.  Run the `flush_caches.sh` script in this repo to help clear them out and re-run your tensorflow script.


### Questions:

1. In your own words, what is a **bottleneck**?
2. In this lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
3. How does a low `--learning_rate` (step 7) value (like 0.005) affect the precision? How much longer does training take?
4. How about a `--learning_rate` (step 7) of 1.0? Is the precision still good enough to produce a usable graph?
5. For section 8, you can use any images you like. Pictures of food, people, or animals work well. You can even find images at ImageNet. How accurate was your model? Were you able to train it using a few images, or did you need a lot?
6. Run the script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)?
7. Try the training again, but this time do `export ARCHITECTURE="inception_v3"` Do you notice the CPU vs GPU difference now?


### To turn in:
Turn in a text file or pdf with your answers to the questions above.

