# Lab 1: More Docker and YOLO

Docker is great for projects since you can place and run everything you need in a container through a easy, reproducible process. We'll use Docker to build and run our very own container with Darknet and YOLO.

This lab is run on the Xavier device using the desktop (via VNC or display).

Ensure that you cloned this github repo and are in the directory for this lab (v2/week01/lab/).

## Intro to YOLO
[YOLO v5](https://github.com/ultralytics/YOLOv5) was created by Ultralytics, a U.S.-based particle physics and AI startup with over 6 years of expertise supporting government, academic and business clients. It is the latest version of the You Only Look Once framework.
 

## Using YOLO with Docker
With Docker, we can run YOLO entirely self-contained instead of downloading Darknet and other dependencies manually.

### Docker Basics
Some Docker terminology: An image is the program that you develop in Docker. A container is an instance of an image that you actually run. A traditional programming analogy would be that an image is a class, and a container is an object of that class. Images are created using Dockerfiles and can be stored and pulled from online repositories. Boot up the Xavier, open a terminal, and list the current images on the Xavier:

```
docker images
```
You'll likely see the arm64/hello-world image created in HW #1. "latest" is the default tag of an image if you don't specify it. The image ID is the best way to refer to a image. Now show all containers:

```
docker ps -a
```
There should be a container with "hello-world" listed under the "IMAGE" column, based off the hello-world image we just saw. Containers also have IDs as well as names (different from an image's tag) that are randomly generated if not specified.

### Creating a Docker Image with a Dockerfile
This Dockerfile creates a container that will run YOLO-v5. It will download the model based on the `MODEL` environment variable you will create (further down in this lab). Build the image:

```
docker build -t yolov5 -f Dockerfile.yolov5 .
```
Wait for the process to finish, then list the Docker images to see if it worked. You should see a new image with the label "YOLO" under the repository column.

### Running YOLO with a Container
Connect a USB webcam to the Xavier. First, enable X so that the container can output to a window.

```
xhost +
```
Now create and run a container with YOLO, starting with regular YOLO first:

```
MODEL=yolov5x.pt
CAM=0
docker run --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -ti yolov5 python3 detect.py --source $CAM --weights $MODEL --conf 0.4
```

A new window should open with live video feed from the webcam. The terminal window displays FPS and objects detected with percentage of how sure YOLO thinks it's right. What FPS do you get? Try running YOLO with the smaller model:

```
MODEL=yolov5s.pt
CAM=0
docker run --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -ti yolov5 python3 detect.py --source $CAM --weights $MODEL --conf 0.4
```
What is the FPS now?

Was one of the models more accurate?

These containers automatically delete themselves after you exit due to the "--rm" flag. Containers tend to pile up if you don't manage them well. If you want to look inside the running container, omit the command that automatically opens YOLO upon running the container and add the flag "-ti" to enter interactive mode:

```
docker run -e DISPLAY=$DISPLAY --rm  --privileged -v /tmp:/tmp -ti yolov5
```
Now you can explore with regular terminal commands.

