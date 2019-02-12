# Labs 8: Ways to build an image data set.

This lab will cover some ways of buildig an image data set.  

## Attention
This lab requires a Flickr API key.  Please requrest a key at https://www.flickr.com/services/apps/create/apply/.

## Setup 
You'll be using a docker image for this lab and it is recommended that you run this on your workstation.

1. Create a data directory for the images.
2. Start the docker image
```bash docker run -ti -v <pathToYourDataDiretory>:/images/data ryandejana/lab8:v1 bash ```

## Part 1: FFMPEG and Video
In the first part of this lab, you'll work with a video from https://www.jpjodoin.com/urbantracker/dataset.html and you'll be extracting images from it.

In the directory /images, you'll find the file sherbrooke_video.avi.  This is a 2 min and 13 second video filmed from a traffic camera located at at the Sherbrooke/Amherst intersection in Montreal.

The first step is to extract a single image from the video.

```bash ffmpeg -i sherbrooke_video.avi -frames:v 1 data/ffmepg/test1/extracted.jpg```

the option ```-frames:v``` specifies the number of frames to extract and ```data/ffmepg/test1/extracted.jpg``` is the output file.  

When complete, browser your data directory from your workstation and open up ```data/ffmepg/test1/extracted.jpg``` and confirm that extract.

Now you wille extract 100 images from the file using the command 
```bash ffmpeg -i sherbrooke_video.avi -frames:v 100 data/ffmepg/test2/extract%04d.jpg```

With this command, ```%04d``` tells ffmpeg to name the extracted images with the serices with a 4 digit pattern, extract0001.jpg, extract0002.jpg, etc. Other numbers may be used, e.g. to use 2 numbers, the pattern would be ```%02d```.

Review the images.  How much did the scence change?

Now we'll adjust the frames per second used with the -r option, in this case with 1 frame per second.

```bash ffmpeg -i sherbrooke_video.avi -frames:v 100 -r 1 data/ffmepg/test2/extract%04d.jpg```

What's different?  What happens if you change r?

Finally, we'll extract all the images with the command
```bash ffmpeg -i sherbrooke_video.avi data/ffmepg/test3/extract%04d.jpg```

How long did it take?  How many images did you get?  Which is the "best" approach?

## Part 2a: Downloading images

