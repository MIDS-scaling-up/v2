## Yolo on Xavier
Just a few differences compared to tx2: we need to use the dev container as the base and we compile OpenCV as opposed to using the apt version. Otherwise the same.

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
docker run -e DISPLAY=$DISPLAY --rm  --privileged -v /tmp:/tmp yolo ./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights -c 1
```
A new window should open with live video feed from the webcam. The terminal window displays FPS and objects detected with percentage of how sure Yolo thinks it's right. What FPS do you get? Try running tiny-yolo:
```
docker run -e DISPLAY=$DISPLAY --rm  --privileged -v /tmp:/tmp yolo ./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights -c 1
```
What is the FPS now?
These containers automatically delete themselves after you exit due to the "--rm" flag. Containers tend to pile up if you don't manage them well. If you want to look inside the running container, omit the command that automatically opens Yolo upon running the container and add the flag "-ti" to enter interactive mode:
```
docker run -e DISPLAY=$DISPLAY --rm  --privileged -v /tmp:/tmp -ti yolo
```
Now you can explore with regular terminal commands.

