# Labs 4: Keras / Theano MNIST demo (20 min in teams)
In this lab, we take the same concept to the familiar world of Jupyter and Keras.  This lab, as the previous ones, should be done 
in groups.  Note the number of your group, and open up the corresponding url; e.g. if your group number is 4, then go to http://169.44.201.108:8891/notebooks/cnn4.ipynb   The instructors will provide you with the Jupyter token.
Familiarize yourself with the code.  Make sure you understand the meaning of the layers in the model definition.  Run the model to completion, then try the following:
* Note the time difference between GPU and CPU training (change the parameter in cell 1).  Note that multiple teams may be using the same GPU at the same time.  There are two GPUs in this machine, and we've assigned teams 1,3,5 GPU 0 and teams 2,4,6 GPU 1; ideally, only one team should be using the GPU at a time. 
* Familiarize yourself with the MNIST dataset
* How many samples are there? How many for training? How many for testing?
* Note the differences in network architecture vs the convnetjs homework
* Which model is more accurate?
* Increase the batch size when using the CPU.  Does this improve training speed?
* Do the same using the GPU.  What happens?
* What does dropout do?
* How many epochs to do you need to fully train your network?
* How can you improve it?
* Can you get more than 99% accuracy?
* What is overfitting?
* Can you name the techniques that would help you reduce overfitting?

