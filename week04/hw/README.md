# Homework 4: DL 101

#### 1. Classification of a 2D dataset using ConvnetJS
ConvnetJS is a very simple yet powerful JavaScript library for Convolutional Neural Networks created by Andrei Karpathy, previously a Graduate Student at Stanford (under Fei-Fei Li) 
and now the leader of the Autonomous Driving project at Tesla.  The library runs directly in the browser and uses the CPU of your computer for training (just one core, so it will be woefully slow on large networks).  It is highly interactive, however, and enables you to rapidly experiment with small nets. You can read more about ConvNetJs and its api at http://cs.stanford.edu/people/karpathy/convnetjs/
Our first lab aligns with the 2D classification example available here: http://cs.stanford.edu/people/karpathy/convnetjs/demo/classify2d.html
Once you hit this page, the network starts running.  
* Add a few red dots in previously green areas by clicking the left mouse button.  Is the network able to adjust and correctly predict the color now?
* Add a few green dots in previously red areas by clicking the shift left mouse button.  Can the network adapt?
* Review the network structure in the text box.  Can you name the layers and explain what they do?
* Reduce the number of neurons in the conv layers and see how the network responds. Does it become less accurate?
* Increase the number of neurons and layers and cause an overfit.  Make sure you understand the concept
* Play with activation functions.. -- relu vs sigmoid vs tanh... Do you see a difference ? Relu is supposed to be faster but less accurate.

#### 2. ConvnetJS MNIST demo
In this lab, we will look at the processing of the MNIST data set using ConvnetJS.  This demo uses this page: http://cs.stanford.edu/people/karpathy/convnetjs/demo/mnist.html
The MNIST data set consists of 28x28 black and white images of hand written digits and the goal is to correctly classify them.  Once you load the page, the network starts running and you can see the loss and predictions change in real time.  Try the following:
* Name all the layers in parameters in the network, make sure you understand what they do.
* Experiement with the number  and size of filters in each layer.  Does it improve the accuracy?
* Remove the pooling layers.  Does it impact the accuracy?
* Add one more conv layer.  Does it help with accuracy?
* Increase the batch size.  What impact does it have?
* What is the best accuracy you can achieve?


#### Submission:
Please submit answers to #2
