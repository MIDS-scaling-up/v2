# HW 3: Creating a Dataset and Transfer Learning

In the previous week, we used the ImageNet database to train GoogLeNet and saved the resultant model onto out Jetson. Now we'll use this model, make our own dataset, and create a live video feed sign language translator. 

## Intro to Transfer Learning
Transfer learning is the use of a model trained on one task for another related task. Training a new model and weights takes a long time, uses enormous computing power, and requires a very large amount of relevant data. Transfer learning is useful when you have smaller amounts of data for a task related to the original one. In this case, we'll create our own dataset of sign language symbols and repurpose the pretrained GoogLeNet model for a new sign language classifer/translator model. 

## Setting Up the Dataset and DIGITS
We first need a dataset of sign language images to train the model on. Then we'll mount the dataset and pretrained model in the DIGITS container for usage.

### Extracting Images from Videos
We'll use 10 classes for the dataset, each representing one sign language symbol. Here is the alphabet for reference:
<img src="https://www.startasl.com/wp-content/uploads/startasl/550x712xsign-language-alphabet.jpg">

It would take too long to take individual pictures, so instead we'll extract an image sequence from a video. Using your phone or any video recorder, record ten videos each around 10 seconds. In each video, record your hand performing a different sign language symbol. While recording, ensure the symbol is the dominant object in the frame and try to vary the video by moving your hand around, changing the background, etc. This is so there is more variety in the images. 

Once done, move the videos to the Jetson by your preferred method (Google Drive, Dropbox, etc). Now open a terminal and install ffmpeg, which can extract images from videos. 
```
sudo apt-get install ffmpeg
```
Enter the folder where the videos are stored on the Jetson. Create a directory for each video, properly labelled with the symbol they correspond to, and place the videos inside their corresponding directory. The image labels of these directories will be what the model is trained on and outputs during inferencing. Now visit each one of these directories and extract all the images using this command for each video:
```
ffmpeg -i <video-file-name> <output-image>_%03d.png
```
You can replace <output-image> with a name that makes sense to you (likely the symbol name), and the trailing "%03d" automatically numbers the resulting images. This process should result in a few hundred images for each symbol. Move the videos out of the directories so that they aren't mixed up when DIGITS is creating the dataset. Take all the directories holding the symbol images and place them all in a new  directory called "images" for referencing later on. Take a look at the ImageNet dataset used last week and make sure your sign language dataset looks similar to it. This is the format DIGITS expects datasets to be in when it creates one.

### Transfering the Dataset and Pretrained Model to DIGITS
First, the pretrained model must be in the right format to be used by DIGITS. The Jetson and the VS can't properly use models between each other, as noted last week. To fix this, find the .tar pretrained model file downloaded from DIGITS on the VS. Untar the file and locate the .caffemodel file from the results. Create a new directory called "data" to hold this pretrained model file, and place the "images" directory with all the sign language symbol images that you made in the previous section inside this same directory. This "data" directory will be mounted to the DIGITS container so DIGITS can access the sign language dataset and the .caffemodel pretrained model file.

Finally, create a new DIGITS container, mounting the "data" directory to a new /data directory in the DIGITS container (replace the <> with the path to the directory):
```
docker run --privileged -i -p 5001:5001 -d -v </path/to/data>:/data digits
```
Now open DIGITS in a browser and select the option to create a new "Classification" dataset. This time, in the "Training Images" section, put `/data/images`. This is where the sign language dataset exists in the DIGITS container. Give a group and dataset name and create the dataset.

## Training a Model on the Sign Language Dataset 

With the sign language dataset and pretrained model loaded into DIGITs, we can now perform transfer learning. 

### Transfer Learning with the Pretrained Model
Select the option to create a new "Classification" model. Choose the sign language dataset created in the previous section and leave the upper half options as their default. Now in the bottom half, choose the "Custom Network" tab. You'll see a large blank space to paste a custom network. 

Go back to the Jetson's local files and find the untarred files from the pretrained model downloaded from DIGITS on the VS. Locate the "original.prototxt" file and open it. Using the find and replace feature, find all instances of "loss<>/classifier" (the <> are usually the numbers 1, 2, or 3). Rename each instance (something like "...classifier_retrain" is enough). This is necessary since the original GoogLeNet was meant for 1000 classes, so the default layers look for such. Our dataset only has 10 classes, so the layers have to be renamed to new ones to randomize the weights.

Copy+paste the modified "original.prototxt" text file into the "Custom Network" blank space. If you like, click "Visualize" to see how the many layers are arranged. In the "Pretrained models" section, put `/data/<.caffemodel-file>`, replacing the <> with the name of the .caffemodel file. Create the model.

### Results and Downloading the Model
Once training is finished, take a look at the graphs. What are the values for top accuracy and top-5 accuracy? How many epochs did it take for these accuracy rates to peak? Once finished, download the model onto the Jetson for use in the lab.
