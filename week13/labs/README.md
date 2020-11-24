# Labs 13: Running Deep Learning applications end to end
Even though we are at the end of 2020, it's impossible not to observe that running end to end DL applications remains suprisingly complex. Perhaps the rapid rate at which new frameworks are being developed is to blame.  Another aspect could be that a lot of time the focus is on the data science aspects only - e.g. on the development of new models, but not on the development of end to end applications. 

In this session, we will review:
* Nvidia Digits - a slightly dated but still, a ridiculously easy to use tool for training and inference.  Note that the [Nvidia Jarvis](https://developer.nvidia.com/nvidia-jarvis) project is supposed to be the successor to [DIGITS](https://developer.nvidia.com/digits).
* The DeepStream SDK, a bleeding edge yet not-so-easy-to use tool for processing multiple video streams in real time, 
* Dusty Franklin's framework - initially designed for inference only on the Jetson family of devices but now extended to do some training as well.


### DeepStream SDK (the official one)
* The [documentation](https://developer.nvidia.com/deepstream-sdk)
* The [Smart Parking Application](https://github.com/NVIDIA-AI-IOT/deepstream_360_d_smart_parking_application/tree/master/perception_docker)
* The [blog post](https://devblogs.nvidia.com/multi-camera-large-scale-iva-deepstream-sdk/) on multi-camera applications
* The [docker container](https://ngc.nvidia.com/catalog/containers/nvidia:deepstream-l4t)
#### NX Instructions
Grab the container:
```
docker run -it --rm --net=host --runtime nvidia  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/deepstream-l4t:5.0.1-20.09-samples
```
Run the 12-camera example:
```
cd samples
deepstream-app -c configs/deepstream-app/source12_1080p_dec_infer-resnet_tracker_tiled_display_fp16_tx2.txt
```
You shoud see 12 screens tracking objects simultaneously.

Now run the people detection demo:
```
docker run -it --rm --net=host --runtime nvidia -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/deepstream-peopledetection:r32.4.2  deepstream-test5-app -c deepstream-5.0/samples/configs/deepstream-app/sourceX_1080p_dec_infer-resnet_tracker_tiled_display_int8_hq_dla_nx.txt
```

### Deep Learning SDK (the unofficial one, by Dustin Franklin)
Let's just prepare the codebase on the Jetson directly:
```
# borrowing from https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo.md

# in case you don't have these.. 
sudo apt-get install git cmake libpython3-dev python3-numpy 
# go to the directory of your choosing
cd 
# clone the repo
git clone https://github.com/dusty-nv/jetson-inference.git
cd jetson-inference
git submodule update --init
mkdir build
cd build
sudo cmake ../
sudo make -j6
sudo make install
```


#### Notes
* As you are exploring, just download all networks for image classification, object detection, segmentation when prompted.
* On the nx, your camera will be flipped until you follow [these instructions](https://devtalk.nvidia.com/default/topic/1023180/jetson-tx2/imagenet-camera-gets-reverse-orientation-image-on-tx2-with-tr2-1/2) to flip it.
* Check out the [models](https://github.com/dusty-nv/jetson-inference#pre-trained-models) that Dusty's framework supports. The model downloader tool could be used at any time to download more!
* It possible to switch between the on-board (Argus) and external USB (v4l2) camera using the flags such as --camera=/dev/video1 --width=640 --height=480 --network=resnet-18 
* There is a lot of information in this repo, take some time to go through it!

#### Running
* Run the camera demo, e.g. ```./camera-viewer``` . See the notes section if your view is flipped. Close the window to exit the program.
* Run the frame classification demo, e.g. ```./imagenet-camera```.  Be patient if you see a lot of debug output, as it's converting the weights to the TensorRT format.  What is the framerate you are getting? Try [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-camera.md)
* Run the object detection demo, e.g. ```./detectnet-camera```. What is the framerate now?  Experiment with [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-camera-2.md)
* Try to image segmentation demo as well: ```./segnet-camera``` Experiment with [other networks](https://github.com/dusty-nv/jetson-inference/blob/master/docs/segnet-console.md)
* Remember the homework? Let's go back to [your trained model](https://github.com/dusty-nv/jetson-inference/blob/7e81381a96c1ac5f57f1728afbfdec7f1bfeffc2/docs/pytorch-plants.md) and continue. Convert our model to the ONNX format, and run imagenet-camera against it. 


