# Week 7 HW TensorRT fun
**This homework is optional and will not be graded**

1. Please peruse [materials on TensorRT](https://developer.nvidia.com/blog/speeding-up-deep-learning-inference-using-tensorrt/)
1. Build the docker container in the docker folder (or `docker pull w251/trt:nx`) and run it, e.g. `docker run --rm -p 8888:8888 --runtime nvidia -v /data:/data -d w251/trt:nx`. 
1. Open and run to completion the yolov3_trt.ipynb
1. Your assignment is to modify this notebook and associated code to work with a YOLOv3-416 model - instead of the default Yolov3-608 model
