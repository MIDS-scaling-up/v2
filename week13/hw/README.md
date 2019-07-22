# Homework 13: Deep Learning SDK (the unofficial one, by Dustin Franklin)

* Review the [github repo](https://github.com/dusty-nv/jetson-inference)
* Review the Docker file (Dockerfile.inf) required the build the container
* Try building on the TX2, e.g. ``` docker build -t inf -f Dockerfile.inf .``` This may take a while.
* Start the container in interactive mode, e.g.
```
xhost +
docker run --rm --privileged -v /tmp:/tmp -v /var:/var -v /home/nvidia/models:/models --net=host --ipc=host --env DISPLAY=$DISPLAY -ti w251/inf:dev-tx2-4.2_b158 bash



