# Labs 13: Inference

1. DeepStream SDK

2. Deep Learning SDK (by Dustin Franklin)
* Review the [github repo](https://github.com/dusty-nv/jetson-inference)
* Review the [docker file])(Dockerfile.inf) required the build the container
* Start the container in interactive mode, e.g.
```
docker run --rm --privileged -v /tmp:/tmp -v /var:/var -v /home/nvidia/models:/models --net=host --ipc=host --env DISPLAY=$DISPLAY -ti w251/inf:tx2-3.3_b39 bash
cd aarch64/bin
```
* Run the camera demo, e.g. ```./gst-camera``` . Close the window to exit the program.
* Run the frame classification demo, e.g. ```./imagenet-camera```.  What is the framerate you are getting?
* Run the object detection demo, e.g. ```./detectnet-camera```. What is the framerate now?
* Try to image segmentation demo as well: ```./segnet-camera```


