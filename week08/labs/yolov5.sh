#!/bin/sh

xhost +

MODEL=yolov5x.pt
CAM=0
docker run --privileged --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -ti yolov5 python3 detect.py --source $CAM --weights $MODEL --conf 0.4


