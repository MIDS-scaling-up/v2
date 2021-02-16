# Homework 7  Neural face detection pipeline

### Overview
The objective of this homework is simple: modify the processing pipeline that you implemented in 
[homework 3](https://github.com/MIDS-scaling-up/v2/blob/master/week03/hw/README.md) and replace the OpenCV-based face detector with 
a Deep Learning-based one. You could, for instance, use the materials from 
[FaceNet lab 6](https://github.com/MIDS-scaling-up/v2/tree/master/week06/labs/facenet-lab)


### Hints
* You have the freedom to choose the neural network that does the detection, but don't overthink it; this is a credit / no credit assignment that is not supposed to take a lot of time.
* There is no need to train the network in this assignment, just find and use a pre-trained model that is trained on a face dataset.
* Your neural detector should run on the Jetson.
* Just like the OpenCV detector, your neural detector needs to take a frame as input and return an array of rectangles for each face detected.
* Most neural object detectors operate on a frame of a given size, so you may need to resize the frame you get from your webcam to that resolution.
* Note that face detection is not the same as face recognition; you don't need to discriminate between different faces


### Questions
* Describe your solution in detail.  What neural network did you use? What dataset was it trained on? What accuracy does it achieve?
* Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
* What framerate does this method achieve on the Jetson? Where is the bottleneck?
* Which is a better quality detector: the OpenCV or the neural one?

### To turn in:

Please provide answers to questions above, a copy of the code related to the neural face detector along with access to the location (object storage?) containing the detected face images. Note that this homework is NOT graded, credit / no credit only.
