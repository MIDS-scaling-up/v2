# Homework 13: Deep Learning SDK (the unofficial one, by Dustin Franklin)

We find that Dusty's repo has been one of the best places to find cool examples and cool code for doing something practical, so hopefully you'll enjoy it as well.  In this homework, you'll be using transfer learning to create a model that classifies plants, directly on your TX2!

## Setting up

* Review the [github repo](https://github.com/dusty-nv/jetson-inference)
* Review the Docker file (Dockerfile.inf) required the build the container
* Try building on the TX2, e.g. ``` docker build -t inf -f Dockerfile.inf .``` This will take a few minutes.
* Start the container in interactive mode, e.g.
```
# this needs to be done on the jetson
xhost +
docker run --rm --privileged -v /tmp:/tmp -v /data:/data -v /var:/var -v /home/nvidia/models:/models --net=host --ipc=host --env DISPLAY=$DISPLAY -ti w251/inf:dev-tx2-4.2_b158 bash
```
* Pytorch and torchvision should already be installed for you, just make sure you use python3 for all commands instead of regular python (which points to python2)
* Swap should also be already set up for you ( we did this in homework 1)

## Training the model
We suggest that you generally follow [these instructions](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-plants.md) to train ResNet-18 on the PlantCLEF dataset.  Just a few notes:
* Review the [train script](https://github.com/dusty-nv/pytorch-imagenet/blob/master/train.py)
* Once again, please use python3 for all commands
* Note that in the instructions above, you passed through /data to your container.  Create the dataset directory, download the dataset / uncompress there.
* Train for 100 epochs 
* You are running on the tx2, so the training will take less time than on the nano (which is what Dusty benchmarked on)

## To submit
Please submit the time it took you to train the model along with the final accuracy top1/top5 that you were able to achieve. Could you increase the batch size? Why? How long did the training take you? Please save your trained model, we'll use it for the lab.


Credit / no credit only




