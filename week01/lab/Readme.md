# Lab 1: More Docker and Yolo

Docker is great for projects since you can place and run everything you need in a container through a easy, reproducible process. We'll use Docker to build and run our very own container with Darknet and Yolo.

## Intro to Darknet and Yolo
[Darknet](https://pjreddie.com/darknet/) is an open source neural network framework that can run both CPU and GPU computation. The project developer provides a variety of uses for it, the most prominent being an object detection/classification system called Yolo. Yolo is fast and accurate for its size, using a single neural network to look at an entire image instead of scanning frames. This makes it great for low-power, IoT platforms just like the Jetson. 

## Using Yolo with Docker
With Docker, we can run Yolo entirely self-contained instead of downloading Darknet and other dependencies manually.

### Docker Basics
Some Docker terminology: An image is the program that you develop in Docker. A container is an instance of an image that you actually run. A traditional programming analogy would be that an image is a class, and a container is an object of that class. Images are created using Dockerfiles and can be stored and pulled from online repositories. Boot up the Jetson, open a terminal, and list the current images on the Jetson:
```
docker images
```
You'll likely see the arm64/hello-world image created in HW #1. "latest" is the default tag of an image if you don't specify it. The image ID is the best way to refer to a image. Now show all containers:
```
docker ps -a
```
There should be a container with "arm64/hello-world" listed under the "IMAGE" column, based off the hello-world image we just saw. Containers also have IDs as well as names (different from an image's tag) that are randomly generated if not specified.

### Creating a Docker Image with a Dockerfile
This Dockerfile downloads yolo as well as tiny-yolo, which is a condensed version of Yolo that runs faster but is less accurate. cd into the directory with this Dockerfile, download the Makefile on Github in the week1/lab directory, and place it in here. Build the image:
```
docker build -t yolo -f Dockerfile.yolo .
```
Wait for the process to finish, then list the Docker images to see if it worked. You should see a new image with the label "yolo" under the repository column.

### Running Yolo with a Container
Connect a USB webcam to the Jetson. First, enable X so that the container can output to a window.
```
xhost local:root
```
Now create and run a container with Yolo, starting with regular Yolo first:
```
xhost local:root
docker run -e DISPLAY=$DISPLAY --privileged -v /tmp:/tmp --rm --env QT_X11_NO_MITSHM=1 yolo ./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights -c 1
```
A new window should open with live video feed from the webcam. The terminal window displays FPS and objects detected with percentage of how sure Yolo thinks it's right. What FPS do you get? Try running tiny-yolo:
```
docker run -e DISPLAY=$DISPLAY --privileged -v /tmp:/tmp --rm --env QT_X11_NO_MITSHM=1 yolo ./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights -c 1
```
What is the FPS now?
These containers automatically delete themselves after you exit due to the "--rm" flag. Containers tend to pile up if you don't manage them well. If you want to look inside the running container, omit the command that automatically opens Yolo upon running the container and add the flag "-ti" to enter interactive mode:
```
docker run -e DISPLAY=$DISPLAY --rm  --privileged -v /tmp:/tmp -ti yolo
```
Now you can explore with regular terminal commands.

