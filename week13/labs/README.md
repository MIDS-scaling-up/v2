# Labs 13: Inference and End to End

1. DeepStream SDK
* The [documentation](https://developer.nvidia.com/deepstream-sdk)
* The [Smart Parking Application](https://github.com/NVIDIA-AI-IOT/deepstream_360_d_smart_parking_application/tree/master/perception_docker)
* The [blog post](https://devblogs.nvidia.com/multi-camera-large-scale-iva-deepstream-sdk/) on multi-camera applications
* The [docker containeer](https://ngc.nvidia.com/catalog/containers/nvidia:deepstream)

2. Deep Learning SDK (by Dustin Franklin)
* Review the [github repo](https://github.com/dusty-nv/jetson-inference)
* Review the Docker file (Dockerfile.inf) required the build the container
* Try building on the TX2, e.g. ``` docker build -t inf -f Dockerfile.inf .``` This may take a while and provided for reference only, so you could modify it in the future. You can complete this in your own free time; kill it before continuing to the next step
* Start the container in interactive mode, e.g.
```
docker run --rm --privileged -v /tmp:/tmp -v /var:/var -v /home/nvidia/models:/models --net=host --ipc=host --env DISPLAY=$DISPLAY -ti w251/inf:tx2-3.3_b39 bash
cd aarch64/bin
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


