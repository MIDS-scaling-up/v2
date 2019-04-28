# Labs 13: Inference and End to End

### DeepStream SDK (the official one)
* The [documentation](https://developer.nvidia.com/deepstream-sdk)
* The [Smart Parking Application](https://github.com/NVIDIA-AI-IOT/deepstream_360_d_smart_parking_application/tree/master/perception_docker)
* The [blog post](https://devblogs.nvidia.com/multi-camera-large-scale-iva-deepstream-sdk/) on multi-camera applications
* The [docker container](https://ngc.nvidia.com/catalog/containers/nvidia:deepstream)

Provision a VM with a P-100 in Soflayer per the [instructions in HW3](https://github.com/MIDS-scaling-up/v2/tree/master/week03/hw)  In this case, you will need CUDA 10.0, not CUDA 10.1 Make sure that you install docker and then nvidia-docker.

We will be running DeepStream SDK in the cloud obviously but would still like to see the output locally.  So, let's configure the remote desktop:
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
# this is the latest ATM and it depends on Cuda 10.0, sigh
nvidia-docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -w /roo/tDeepStream_Release/samples nvcr.io/nvidia/deepstream:3.0-18.11
```

Since we are using a P-100 card (we are cheap!), we need to change to default inference mode from Int8 to Int32. The inference precision is set using the network-mode setting (1=INT8, 0 = FP32). Therefore, all entries in the above config files reading: ```network-mode=1``` have to be changed to: ```network-mode=0```
```
These are the files we need to change:

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
* Review the [github repo](https://github.com/dusty-nv/jetson-inference)
* Review the Docker file (Dockerfile.inf) required the build the container
* Try building on the TX2, e.g. ``` docker build -t inf -f Dockerfile.inf .``` This may take a while and provided for reference only, so you could modify it in the future. You can complete this in your own free time; kill it before continuing to the next step
* Start the container in interactive mode, e.g.
```
xhost +
docker run --rm --privileged -v /tmp:/tmp -v /var:/var -v /home/nvidia/models:/models --net=host --ipc=host --env DISPLAY=$DISPLAY -ti w251/inf:tx2-3.3_b39 bash
```
Note: this demo will, by default, use the on-board camera.  If you wish to use the external USB camera, you will need to edit the corresponding source -- e.g. /jetson-inference/detectnet-camera/detectnet-camera.cpp or imagenet-camera/imagenet-camera.cpp and change the DEFAULT_CAMERA variable to the index of your USB camera.  For instance, the first USB camera should be /dev/video1 (the /dev/video0 camera should be the built in one), so DEFAULT_CAMERA should be set to 1 

Also, some USB cameras do not support the default resolution for this code, which is set to 1280x720 in utils/camera/gstCamera.h:
```
	static const uint32_t DefaultWidth  = 1280;
	static const uint32_t DefaultHeight = 720;
```
Tweak these (640x480 is a safe bet) if you see related errors while trying to run.  

Once you change the source, you need to recompile:
```
cd /jetson-inference/build
make install
```

* Run the camera demo, e.g. ```./gst-camera``` . Close the window to exit the program.
* Run the frame classification demo, e.g. ```./imagenet-camera```.  What is the framerate you are getting? Try [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-camera.md)
* Run the object detection demo, e.g. ```./detectnet-camera```. What is the framerate now?  Experiment with [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-camera-2.md)
* Try to image segmentation demo as well: ```./segnet-camera``` Experiment with [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/segnet-console.md)
* [Earlier in the class](https://github.com/MIDS-scaling-up/v2/tree/master/week07/hw), we trained a DetectNet model on the Kitti dataset.  Follow [these](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-snapshot.md) and [these](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-custom.md) instructions to use it for inference with the detectnet camera demo. Here's my command line, after downloading one of our student's [model](http://169.44.201.108:5000/models/20190216-223354-6fb5/download):
```
# make sure you move the tgz archive to /jetson-inference/data/networks/kitti/ , decompress, and remove the last layer out of the deploy.prototxt
NET=networks/kitti
./detectnet-camera --prototxt=$NET/deploy.prototxt --model=$NET/snapshot_iter_19140.caffemodel --labels=$NET/labels.txt --input_blob=data 
```


