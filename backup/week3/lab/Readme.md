# Lab 3: Live Camera Inferencing 

In the homework, we used transfer learning on a dataset of sign language symbols to create a new model. Now, we'll use that model on live video feed in a way similar to yolo that will translate sign language hand symbols in real time.

## Setting up a jetson-inference Container

We'll run jetson-inference in a Docker container this time. First, download the "Dockerfile.tensorrt" file and build the TensorRT image:
```
docker build -t tensorrt -f Dockerfile.tensorrt
```
Now download the "Dockerfile.inference" file and build the jetson-inference image:
```
docker build -t inference -f Dockerfile.inference
```
Locate the .tar sign language transfer learning model created in the hw. Untar it and place the resulting contents in a directory. Enable X so the live camera feed window can show up, then create a docker container for jetson-inference mounted with the directory holding the untarred sign language model:
```
xhost +
docker run --privileged -v /dev:/dev -e DISPLAY=$DISPLAY -v /tmp:tmp --net=host --ipc=host --ti -v </path/to/directory>:/data inference
```
Now within the container, move to the /jetson-inference/build/aarch64/bin directory and run jetson-camera with the following options to enable the sign language model. Like before, set NET to the location of the untarred model (in this case /data) and make sure the --model option has the correct .caffemodel file name:
```
NET=</datal>
./imagenet-camera \
--prototxt=$NET/deploy.prototxt \
--model=$NET/<snapshot_iter_file> \
--labels=$NET/labels.txt \
--input_blob=data \
--output_blob=softmax
```
After a short while, a window should appear with live camera feed from the Jetson's built-in camera and the inference guess of the object in the frame near the top of the window. Try showing the camera some sign language hand symbols you trained the model on. How accurate is it? 

