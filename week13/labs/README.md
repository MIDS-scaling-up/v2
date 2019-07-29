# Labs 13: Running Deep Learning applications end to end
Even though we are in the middle 2019, it's impossible not to observe that running end to end DL applications remains suprisingly complex. Perhaps the rapid rate at which new frameworks are being developed is to blame.  Another aspect could be that a lot of time the focus is on the data science aspects only - e.g. on the development of new models, but not on the development of end to end applications. 

In this session, we will review:
* Nvidia Digits - a slightly dated but still, a ridiculously easy to use tool for training and inference
* The DeepStream SDK, a bleeding edge yet not-so-easy-to use tool for processing multiple video streams in real time, 
* Dusty Franklin's framework - initially designed for inference only on the Jetson family of devices but now extended to do some training as well.

### Nvidia Digits Review
Some of you may have already done these, but in case you didn't, this is the time!
* [Introduction to Digits on the TX2](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/intro-digits-tx2.md). Digits wasn't supposed to be run on the TX2, but we can!
* [Fine tuning GoogleNet with Digits](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_digits.md). Note that it does not take long to fine tune, especially if you know what you are doing and know how to freeze weights!
* [Object Detection with Digits](https://github.com/MIDS-scaling-up/v2/tree/master/week07/hw/backup) - review only, we won't be able to complete this in class.  The idea here is to learn that it is possible to train an object detection framework on your own dataset.

### DeepStream SDK (the official one)
* With the just released jetpack 4.2.1 , you should be able to run DeepStream SDK on the jetson; We will run it in the Cloud as it's not compatible with 4.2.0
* The [documentation](https://developer.nvidia.com/deepstream-sdk)
* The [Smart Parking Application](https://github.com/NVIDIA-AI-IOT/deepstream_360_d_smart_parking_application/tree/master/perception_docker)
* The [blog post](https://devblogs.nvidia.com/multi-camera-large-scale-iva-deepstream-sdk/) on multi-camera applications
* The [docker container](https://ngc.nvidia.com/catalog/containers/nvidia:deepstream)

Provision a VM with a P-100 in Soflayer per the [instructions in HW6](https://github.com/MIDS-scaling-up/v2/tree/master/week06/hw), e.g.
```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100a --domain=dima.com --image=2263543 --billing=hourly  --network 1000 --key=1418191 --flavor AC1_8X60X100 --san
```


We will be running DeepStream SDK in the cloud VM obviously but would still like to see the output locally.  So, let's configure the remote desktop:
```
apt update
apt install x11vnc x11-xserver-utils xinit
# We need to use our GPU as a graphics card
nvidia-xconfig --query-gpu-info

# this is what the output should look like: 
# Number of GPUs: 1
# GPU #0:
# Name      : Tesla P100-PCIE-16GB
# UUID      : GPU-5f2b341b-ba97-8909-15cd-22274f1e81d9
# PCI BusID : PCI:0:7:0
# Number of Display Devices: 0
# Note BusID above, e.g. PCI:0:7:0 and replace BUSID with it below
nvidia-xconfig -a --allow-empty-initial-configuration --use-display-device=None --virtual=1920x1200 --busid $BUSID
```
Next, make sure to remove the ServerLayout and Screen sections from /etc/X11/xorg.conf.

Now we should be ready to start our X and VNC server!
```
xinit & 
export DISPLAY=:0
x11vnc -forever -shared -display :0 -passwd <your password> &

# allow our docker container to connect 
xhost +
```
Using the VNC / screensharing client of your choice, connect to the VNC display 0 (port 5900) on your VM. If you are on Windows, you can use TightVNC or TigerVNC.  If you are on a Mac, you can use your screensharing app.

Now, let us start the container:
```
nvidia-docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -w /root/DeepStream_Release/samples nvcr.io/nvidia/deepstream:3.0-18.11
```

Since we are using a P-100 card (we are cheap!), we need to change to default inference mode from Int8 to Int32 for optimal performance as Int8 is not native for a P-100. The inference precision is set using the network-mode setting (1=INT8, 0 = FP32). Therefore, all entries in the above config files reading: ```network-mode=1``` have to be changed to: ```network-mode=0```
```
These are the files we need to OPTIONALLY change:

/root/DeepStream_Release/samples/configs/deepstream-app/config_infer_primary.txt
/root/DeepStream_Release/samples/configs/deepstream-app/config_infer_secondary_carcolor.txt
/root/DeepStream_Release/samples/configs/deepstream-app/config_infer_secondary_carmake.txt
/root/DeepStream_Release/samples/configs/deepstream-app/config_infer_secondary_vehicletypes.txt
```
We are finally ready to run our samples!
```
cd /root/DeepStream_Release/samples
deepstream-app -c configs/deepstream-app/source4_720p_dec_infer-resnet_tracker_sgie_tiled_display_int8.txt

```

### Deep Learning SDK (the unofficial one, by Dustin Franklin)
At of July 2019, this functionality is, yet again in flux (sigh).  Nvidia has just dropped [Jetpack 4.2.1](https://developer.nvidia.com/embedded/jetpack) - which is [supposed to introduce Nvidia docker to the Jetson platform](https://devtalk.nvidia.com/default/topic/1046113/jetson-tx2/can-nvidia-docker-run-on-tx2-/) . But, we can't get the on-board camera to work with our docker container introduced in [the homework](https://github.com/MIDS-scaling-up/v2/tree/master/week13/hw). It is possible that the USB camera works, but we could not test it in time.

So, let's just prepare the codebase on the Jetson directly:
```
# borrowing from https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo.md
# become root
# in case you don't have these.. 
apt install -y git cmake 
# go to the directory of your choosing
cd 
# clone the repo
git clone https://github.com/dusty-nv/jetson-inference.git
cd jetson-inference
git submodule update --init
mkdir build
cd build
cmake ../
make -j6
make install
```


#### Notes
* Check out the [models](https://github.com/dusty-nv/jetson-inference#pre-trained-models) that Dusty's framework supports. The model downloader tool could be used at any time to download more!
* It possible to switch between the on-board (Argus) and external USB (v4l2) camera using the flags such as --camera=[/dev/video0], --width=[640], --height=[480], --network=[resnet-18]
* There is a lot of information in this repo, take some time to go through it!

#### Running
* Run the camera demo, e.g. ```./camera-viewer``` . Close the window to exit the program.
* Run the frame classification demo, e.g. ```./imagenet-camera```.  What is the framerate you are getting? Try [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-camera.md)
* Run the object detection demo, e.g. ```./detectnet-camera```. What is the framerate now?  Experiment with [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-camera-2.md)
* Try to image segmentation demo as well: ```./segnet-camera``` Experiment with [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/segnet-console.md)
* Remember the homework? Let's go back to [your trained model](https://github.com/dusty-nv/jetson-inference/blob/7e81381a96c1ac5f57f1728afbfdec7f1bfeffc2/docs/pytorch-plants.md) and continue. Convert our model to the ONNX format, and run imagenet-camera against it. 
* [Earlier in the year](https://github.com/MIDS-scaling-up/v2/tree/master/week07/hw/backup), w251 students trained a DetectNet model on the Kitti dataset.  Follow [these](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-snapshot.md) and [these](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-custom.md) instructions to use it for inference with the detectnet camera demo. Here's my command line, after downloading one of our student's [model](http://169.44.201.108:5000/models/20190216-223354-6fb5/download):
```
# make sure you move the tgz archive to /jetson-inference/data/networks/kitti/ , decompress, and remove the last layer out of the deploy.prototxt
NET=networks/kitti
./detectnet-camera --prototxt=$NET/deploy.prototxt --model=$NET/snapshot_iter_19140.caffemodel --labels=$NET/labels.txt --input_blob=data 
```


