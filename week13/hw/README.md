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
We suggest that you generally follow [these instructions](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-plants.md) to train ResNet-18 on the PlantCLEF dataset.  Just a few notes:
* Review the [train script](https://github.com/dusty-nv/pytorch-imagenet/blob/master/train.py)
* Once again, please use python3 for all commands
* Note that in the instructions above, you passed through /data to your container.  Create the dataset directory, download the dataset / uncompress there.
* Train for 100 epochs 
* You are running on the tx2, so the training will take less time than on the nano (which is what Dusty benchmarked on)

### Note:
if you see the ```ImportError: cannot import name 'PILLOW_VERSION'``` error, downgrade it:
```
pip3 install Pillow==6.1%
```
## To submit
Please submit the time it took you to train the model along with the final accuracy top1/top5 that you were able to achieve. Could you increase the batch size? Why? How long did the training take you? Please save your trained model, we'll use it for the lab.


Credit / no credit only




