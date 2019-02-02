# Homework 5

## Tensorflow for Poets

For this homework, you need to install Tensorflow on your TX2.

Build the docker container for tensorrt using the Dockerfile [here](https://github.com/MIDS-scaling-up/v2/tree/master/backup/tensorrt)
```
# cd to the correct directory after git cloning the class repo
docker build -t tensorrt -f Dockerfile.tx2-3.3_b39
```

Now build the docker container for tensorflow using the python2 Dockerfile [here](https://github.com/MIDS-scaling-up/v2/tree/master/backup/tensorflow).
```
# cd to the correct directory after git cloning the class repo
docker build -t tensorflow -f Dockerfile.tx2-3.3_b39-py2 .
```


Complete the [Tensorflow for Poets lab](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0) at the Google CodeLabs. Make sure you do all of the optional sections (except section 9).

### Questions:

1. In your own words, what is a **bottleneck**?
2. In this lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
3. How does a low `--learning_rate` (step 7) value (like 0.005) affect the precision? How much longer does training take?
4. How about a `--learning_rate` (step 7) of 1.0? Is the precision still good enough to produce a usable graph?
5. For section 8, you can use any images you like. Pictures of food, people, or animals work well. You can even find images at ImageNet. How accurate was your model? Were you able to train it using a few images, or did you need a lot?
6. Uninstall `tensorflow-gpu` (using `pip uninstall -y tensorflow-gpu`) and install `tensorflow` (follow the instructions at the beginning of the homework, changing the name of the package). How does the training time compare to the default network training (section 4)?


### To turn in:
Turn in a text file or pdf with your answers to the questions above.

