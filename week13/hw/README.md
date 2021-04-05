# Homework 13: Deep Learning SDK (the unofficial one, by Dustin Franklin)

We find that Dusty's repo has been one of the best places to find cool examples and cool code for doing something practical, so hopefully you'll enjoy it as well.  In this homework, you'll be using transfer learning to create a model that classifies plants, directly on your Jetson!

## Set up your default Docker runtime to Nvidia
Edit /etc/docker/daemon.json and add `"default-runtime": "nvidia"`
```
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },

    "default-runtime": "nvidia"
}
```
Now restart docker, e.g. `service docker restart`

## Set up and build the docker image
Review Dusty's [github repo](https://github.com/dusty-nv/jetson-inference), then build the container:
```bash
$ git clone --recursive https://github.com/dusty-nv/jetson-inference
$ cd jetson-inference
$ docker/build.sh
```

## Start the runtime
Assuming we have the image built, let's start it!
```bash
$ docker/run.sh
```

## Training the model
We suggest that you loosely follow [these instructions](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-plants.md) to train at least two networks: ResNet13 and Wide ResNet 50-2 on the PlantCLEF dataset.  Just a few notes:
* Review the [repo](https://github.com/dusty-nv/pytorch-classification) and the [train script](https://github.com/dusty-nv/pytorch-imagenet/blob/master/train.py)
* Please use [the original pytorch example script](https://github.com/pytorch/examples/blob/master/imagenet/main.py) for training as it is more up to date
* Once again, please use python3 for all commands
* Train for 100 epochs 
* ResNet13 / Wide ResNet 50-2 Hint: review the [TorchVision model catalog](https://pytorch.org/vision/stable/models.html)
* Adjust batch size as necessary
* Have you trounced Dusty's results? if not, check your work!


## To submit
Please submit the time it took you to train the model along with the final accuracy top1/top5 that you were able to achieve. Did you get better results with Wide ResNet50 or ResNet13? What training parameters you adjusted? Why? How long did the training take you? Please save your trained model, we'll use it for the lab. Also please review the architecture of the [Wide ResNet 50-2](https://pytorch.org/hub/pytorch_vision_wide_resnet/) network, we will discuss it in class.


Credit / no credit only




