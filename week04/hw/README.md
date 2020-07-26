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
* Name all the layers in the network, describe what they do.
* Experiment with the number  and size of filters in each layer.  Does it improve the accuracy?
* Remove the pooling layers.  Does it impact the accuracy?
* Add one more conv layer.  Does it help with accuracy?
* Increase the batch size.  What impact does it have?
* What is the best accuracy you can achieve? Are you over 99%? 99.5%?

#### 3. Build your own model in Keras
The [Conversation AI](https://conversationai.github.io/) team, a research initiative founded by [Jigsaw](https://jigsaw.google.com/) and Google (both a part of Alphabet) are working on tools to help improve online conversation. One area of focus is the study of negative online behaviors, like toxic comments (i.e. comments that are rude, disrespectful or otherwise likely to make someone leave a discussion).   
  
Kaggle hosted their [second competition](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge#description) on this research. The challenge is to create a model that is capable of detecting different types of of toxicity like threats, obscenity, insults, and identity-based hate better than Perspective’s current models. The competitions use a dataset of comments from Wikipedia’s talk page edits. Improvements to the current model will hopefully help online discussion become more productive and respectful.

We shall be using this dataset to benchmark a number of ML models. 
*Disclaimer: the dataset used contains text that may be considered profane, vulgar, or offensive.*

##### Colab version   

You can run through all the steps; and see how the model is train on the Coversational AI dataset.
At the end you need to load pretrained embeddings from Stanford's GloVe project. Note,
there is a step to download these embeddings in the book.
       
Let's go to the lab at [this link](https://colab.research.google.com/github/MIDS-scaling-up/v2/blob/master/week04/hw/w251_homework04.ipynb).
     
##### Nvidia NX Version    
   
To be continued.     

Now open the notebook and run. And fill in the codes blocks marked for filling in and monitor your AUC. 
For the Logistic regression model you should be getting circa `0.88` AUC and `0.93` or more for the MLP. 

#### Submission:
Please submit answers to #2, and a html download of your completed Jupyter notebook. A link to a github repo is a great way to submit.
 

PLEASE CANCEL YOUR VM ONCE YOU ARE DONE!!!

## Note on cloud usage
![Soflayer](../../softlayer.png?raw=true "Title")
