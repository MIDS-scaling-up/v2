# Face detection using OpenCV and FaceNet PyTorch

### Face Detection

This lab runs on the Xavier device.

In this lab, we will briefly experiment with and compare face detection capabilities of [FaceNet PyTorch](https://github.com/timesler/facenet-pytorch) 
and [OpenCV](https://opencv.org/).

First, please build the docker image using the provided [Dockerfile](Dockerfile):
```
docker build -t facenet -f Dockerfile .
```
Then start the container:
```
docker run --rm --runtime nvidia -p 8888:8888 -ti facenet
```
Open your browser and point it to port 8888.  When prompted for password, enter the token from `docker logs`

Navigate to `facenet_pytorch/examples` ; examine and run `facedetect_cv2.ipynb` . You should already be familiar with this functionality from homework 3.
For now, just observe the accuracy and execution time of this script.

Now, examine and run the `facedetect.ipynb` script. The FaceNet PyTorch library does some face normalization, which impacts performance, but is usually considered 
one of the better / most convenience face detectors out there.
Questions to consider:
* what are the relative performances of the two libraries?
* Does the GPU help facenet?
* What about the accuracies?

### Face Recognition
The facenet library can also perform face recognition. The MTCNN module is pre-trained to perform feature extraction; these features could be then used downstream.
Please review the `examples/finetune.ipynb` script.
Questions:
* How would you modify the script to perform fine tuning on a "real" dataset?
* What would be needed to get started with the lfw dataset?
