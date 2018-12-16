# Lab 2: DIGITS and Inferencing on the Jetson
We've used the cloud to train a model with the Imagenet dataset. Now we'll run inferencing using this trained model on images as well as install DIGITS on the Jetson so it can use this trained model for transfer learning later.

## Inferencing on the Jetson
We can test the trained model on the Jetson by running image inferencing. This is similar to what yolo did, but only to one image instead of a video. NVIDIA has provided a handy program called jetson-inference that does this. 

### Installing jetson-inference
First, make sure git and cmake are installed on the Jetson:
```
apt-get install git cmake
```
Now navigate to the directory where you want jetson-inference stored and retrieve the jetson-inference files:
```
git clone https://github.com/dusty-nv/jetson-inference
```
Configure the files with cmake:
```
cd jetson-inference
mkdir build
cd build
cmake ../
```
Make sure you are still in the build directory, then run `make` to compile the project.

### Running Inference on Images with the Model
Extract the .tar trained model file (check the file name first):
```
tar -xzvf <filename>.tar.gz
```
cd to the jetson-inference/build/aarch64/bin directory, then run inferencing. Set the value of NET to the path of where the extracted trained model files are. You'll also have to check the exact name of the snapshot_iter file, which is part of the extracted files:
```
NET=<path/to/model>
./imagenet-console bird_0.jpg output_0.jpg \
--prototxt=$NET/deploy.prototxt \
--model=$NET/<snapshot_iter_file> \
--labels=$NET/labels.txt \
--input_blob=data \
--output_blob=softmax
```
This will run inference on the bird_0.jpg picture and print the results to the output_0.jpg file. Find the output file and open it. What is the prediction accuracy? Note that the output is labelled according to how the dataset was labelled.

## DIGITS on the Jetson
We'll run DIGITS in a Docker container on the Jetson similar to the VS provisioned in the cloud. Because of this, DIGITS will be accessed on the browser locally instead of through an IP address. 

### Running a DIGITS container on the Jetson
First, create a new directory to store all DIGITS-related Docker content. Ensure you already have the Caffe image built in the hw. Now download the Dockerfile.digits file and build the DIGITS image:
```
docker build -t digits -f Dockerfile.digits .
```
When you run DIGITS, you likely want to pass your data directory through so you won't be copying enormous data sets back and forth.  If you recall, we asked you to add a larger storage device to your Jetson.  Assuming it's mounted to /data, do something like this:
```
mkdir -m 777 /data/digits-data
```

Now, run the DIGITS container, passing your data dir as /data and using host port 5001:
```
docker run --privileged -v /data/digits-data:/data -p 5001:5001 -d digits
```
Open a browser window and go to 0.0.0.0:5001 to access DIGITS running on the Jetson. Note that DIGITS is accessed through "0.0.0.0" instead of the IP address of the VS since it's running on the Jetson. If you need to add large files, copy them to /data/digits-data on the host and they will be visible under /data on the Jetson.

### Uploading a Pretrained Model to DIGITS
Pretrained models are often reused for another task that is related to the original task the model was trained on, which cuts down on time and resources. This is called transfer learning, which will be discussed in more detail during the next week's homework and lab. For now, we will set up the transfer learning procedure on the Jetson by importing the model trained on the VS

Ensure you downloaded the .tar trained model file from DIGITS running on the VS. Open DIGITS running on the Jetson and go to the "Pretrained Models" tab. Choose "Upload Pretrained Model" from the blue "Images" drop-down menu button. Choose "Upload Tar or Zip Archive" in the next window and select the .tar trained model file from DIGITS on the VS. Leave the other values as their default and upload the model. You can now select this model when training a new model, instead of the defaults provided like GoogLeNet. 

However, the pretrained model in this format won't work due to many conflicts in format, version, etc. We'll use a workaround next week when we properly perform transfer learning.
