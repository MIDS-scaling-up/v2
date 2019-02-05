### Digits and Image Classification with Transfer Learning

#### Intro

This assumes that you completed lab 3, have started the digits container and have it running on port 5001.  If you recall, we did something like this:
```
docker run --privileged -v /data/digits-data:/data -p 5001:5001 -d digits
```
Where /data/digits-data resides on your external SD card or a hard drive and has plenty of space.  Let's download a pre-trained googlenet model:
```
# on the Jetson
mkdir /data/digits-data/models
cd /data/digits-data/models
wget http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel
# Now, the model should be visible from inside the digits container as /data/models/bvlc_googlenet.caffemodel
```

In this lab, we are using the Jetson as a tiny inexensive desktop computer with a GPU. It really wasn't meant to be used for model training, but as you will see, it is quite possible.

#### The training set

We prepared an image dataset, it is located here: http://169.44.201.108:7002/tset/ Please take a few minutes to aquaint yourself with it. As you can see, the structure is simple: there is a bunch of directories which correspond to class names, with images underneath that correspond to that class. Note that some directories are empty, and that's OK. Many public data sets share the same structure.

This particular training set is generated via this GUI: http://169.44.201.108:7002/index7.html?c=11071917_foo&date=2017/02/12 This is an experimental project around the surveillance use case. If motion is detected, a simple algorithm localizes it in the frame (draws a bounding box around it) and sends it over to the cloud for manual annotation. Once you have annotated the bounding box, it is added to the training set.

#### Importing the training set into DIGITS 
Access DIGITS at http://ip_of_jetson:5001/
Make sure you are on the DataSets tab. Click on the new data set icon on the right, choose Images -> Classification. Choose Fill as your resize transformation. Select a name for your group name and data set. Set minimum samples per class to 10. Set the URL for the training images to http://169.44.201.108:7002/tset/ and click Create at the bottom.  

Select your new data set from the home page and click Explore training DB.  Take a look at classes and images in them.

#### Training a GoogleNet-based model using transfer learning 
Click on the Models tab and choose New model - > classification. Choose your newly created data set on the left. Select the "custom network" tab. You will need to download the pre-trained model, e.g.

At the bottom, in the pre-trained network field, type "/data/models/bvlc_googlenet.caffemodel". Leave the number of GPUs used at 1. Use the same group name as you used previously for your data set and select a name for your model. In the Custom Network field paste the model from [this link](googlenet_fixed.txt). This is a model with fixed lower layers. Please peruse the file.  Can you tell which layers are frozen? Which layers are unfrozen? Review GoogLeNet arhitecture [in the cs231n slides](http://cs231n.stanford.edu/slides/2017/cs231n_2017_lecture9.pdf).  Also, Click visualize in Digits.  Once you done looking at the architecture, Click OK to close the visialization window. Click Create. How long does it take for the model to exceed 90% accuracy?

#### Training a GoogleNet-based model using transfer learning with unfixed lower layer weights 
Let us repeat the previous steps, but now let us use a network from [this link](googlenet_unfixed.txt). The only difference is that we unfixed the lower layers. Please examine the file and note the differences with the previous one. Now, how long does it take for the model to reach 90% accuracy? 

#### Training a GoogleNet-based model from random weights. 
Let's repeat the previous step using the same custom model but this time, let us clear out the "pre-trained model" field. Now, how long does it take for the model to reach 90% accuracy (trick question alert)?

#### Applying the model to classification 
From the DIGITS homepage, select one of your trained models. At the bottom of the page, under Test a Single Image, pick an image --- feel free to upload your own file. Check the "show visualizations and statistics" checkbox and click "Classify One"
