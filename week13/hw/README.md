# Homework 13: Deep Learning SDK (the unofficial one, by Dustin Franklin)

We find that Dusty's repo has been one of the best places to find cool examples and cool code for doing something practical, so hopefully you'll enjoy it as well.  In this homework, you'll be using transfer learning to create a model that classifies plants, directly on your Jetson!

## Set up your default Docker runtime to Nvidia
``` json
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
We suggest that you generally follow [these instructions](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-plants.md) to train ResNet-34 on the PlantCLEF dataset.  Just a few notes:
* Review the [repo](https://github.com/dusty-nv/pytorch-classification) and the [train script](https://github.com/dusty-nv/pytorch-imagenet/blob/master/train.py)
* Once again, please use python3 for all commands
* Train for 100 epochs 
* Make sure you're training ResNet-34
* You are running on the NX, so the training will take [a lot] less time than on the nano (which is what Dusty benchmarked on)

## To submit
Please submit the time it took you to train the model along with the final accuracy top1/top5 that you were able to achieve. Could you increase the batch size? Why? How long did the training take you? Please save your trained model, we'll use it for the lab.


Credit / no credit only




