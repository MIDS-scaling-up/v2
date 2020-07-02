#!/bin/sh

xhost +

# valid values are: yolov5x.pt yolov5l.pt yolov5m.pt yolov5s.pt

MODEL=yolov5x.pt

# the number of your webcam (0 is the first one plugged in)
CAM=0
docker run --privileged --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -ti yolov5 python3 detect.py --source $CAM --weights $MODEL --conf 0.4


